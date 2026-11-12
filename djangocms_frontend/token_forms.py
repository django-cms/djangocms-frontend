"""Canonical storage for existing adapter-owned form widgets.

Bootstrap widgets may continue posting their native choice values. This boundary
accepts universal values too and writes only normalized known fields to config.
"""

import sys
from copy import deepcopy
from weakref import WeakKeyDictionary

from django import forms
from django.core.exceptions import ValidationError
from entangled.forms import EntangledModelForm as BaseEntangledModelForm

from djangocms_frontend import settings, tokens

# Weak keys: the admin builds a new form class (modelform_factory) for each request.
_project_fields = WeakKeyDictionary()


def project_fields(form_class):
    """Fields of ``form_class`` declared outside djangocms-frontend, e.g. by a project's component.

    Their values belong to the project: they are never converted to or validated as tokens,
    even if they share a token's name. Both spellings of renamed grid keys are included.
    """
    try:
        return _project_fields[form_class]
    except KeyError:
        pass
    names = set()
    config_fields = getattr(getattr(form_class, "_meta", None), "entangled_fields", {}).get("config", ())
    for name, field in form_class.base_fields.items():
        if name not in config_fields:
            continue
        # The declaring class is the first in the MRO, from the base up, that holds the field.
        declaring = (
            cls for cls in reversed(form_class.__mro__) if vars(cls).get("declared_fields", {}).get(name) is field
        )
        owner = next(declaring, None)
        # Forms built with type() get their caller's module (EntangledModelForm.__init_subclass__).
        if owner is not None and not owner.__module__.startswith("djangocms_frontend."):
            names.update((name, tokens.canonical_key(name)))
    _project_fields[form_class] = frozenset(names)
    return _project_fields[form_class]


_plugin_pool = None


def plugin_form(plugin_type):
    """The registered plugin's form class, or None."""
    global _plugin_pool
    if _plugin_pool is None:  # Import once: rendering calls this for each value.
        from cms.plugin_pool import plugin_pool as _plugin_pool
    try:
        form = _plugin_pool.get_plugin(plugin_type).form
    except (KeyError, AttributeError):
        return None
    return form if isinstance(form, type) and hasattr(form, "base_fields") else None


def plugin_project_fields(plugin_type):
    """Config fields a plugin's project form declares itself; they are not tokens."""
    form = plugin_form(plugin_type)
    return project_fields(form) if form is not None else frozenset()


# Modules of the form metaclasses, which a class built with type() reports as its own.
_METACLASS_MODULES = ("django.", "entangled.")


class EntangledModelForm(BaseEntangledModelForm):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # A class built with type() (e.g. GridRowForm) reports its metaclass's module.
        # project_fields() decides field ownership by module, so use the module that
        # called type() instead: the first frame outside the form machinery.
        if cls.__module__.startswith(_METACLASS_MODULES):
            frame = sys._getframe(1)
            while frame is not None and frame.f_globals.get("__name__", "").startswith(
                (*_METACLASS_MODULES, __name__)
            ):
                frame = frame.f_back
            if frame is not None:
                cls.__module__ = frame.f_globals.get("__name__", cls.__module__)

    def __init__(self, *args, **kwargs):
        adapter = settings.token_adapter
        self._token_errors = []
        self._project_fields = project_fields(type(self))
        explicit_initial = dict(kwargs.get("initial") or {})
        self._explicit_config_initial = {tokens.legacy_key(name): value for name, value in explicit_initial.items()}
        if "initial" in kwargs and kwargs["initial"] is None:
            kwargs["initial"] = {}
        # Project bound canonical input onto the adapter's existing widget API.
        args = list(args)
        data = args[0] if args else kwargs.get("data")
        # ModelForm(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance).
        # The canonical key wins over its legacy alias, as in rendering. Without an instance,
        # ModelForm creates one with an empty config.
        instance = args[8] if len(args) > 8 else kwargs.get("instance")
        stored = getattr(instance, "config", None)
        # A non-object config is reported when saving (normalize_config); show an empty form.
        stored, _ = tokens.resolve_aliases(stored if isinstance(stored, dict) else {}, skip=self._project_fields)
        if adapter and data is not None:
            # ModelForm(data, files, auto_id, prefix, ...)
            prefix = args[3] if len(args) > 3 else kwargs.get("prefix")
            if prefix is None:
                prefix = self.prefix
            files = args[1] if len(args) > 1 else kwargs.get("files")

            def data_key(name):
                return f"{prefix}-{name}" if prefix else name

            projected = data.copy()
            values = {}
            for name, field in self.base_fields.items():
                if name in self._project_fields:
                    continue
                # Accept both the widget's own name and its canonical spelling.
                for alias in dict.fromkeys((name, tokens.canonical_key(name))):
                    key = data_key(alias)
                    if key not in data:
                        continue
                    if isinstance(field.widget, forms.MultiWidget):
                        # A single posted key is a whole (canonical) value, not the widget's parts.
                        values[alias] = data[key]
                    else:
                        # Let the widget read its own value, e.g. all values of a multi-select.
                        values[alias] = field.widget.value_from_datadict(data, files, key)
            for name, value in self._project_config(values, report_errors=True, stored=stored).items():
                # Decompose spacing even when projection leaves its native string unchanged.
                # Other unchanged values retain their original (multi-)value representation.
                if name not in self.base_fields:
                    continue
                key = data_key(name)
                widget = self.base_fields[name].widget
                if name in tokens.SPACING_FIELDS and isinstance(value, str) and hasattr(widget, "decompress"):
                    # The widget reads only its parts; drop the posted whole value.
                    projected.pop(key, None)
                    for index, part in enumerate(widget.decompress(value)):
                        projected[f"{key}_{index}"] = part
                    continue
                if name in values and values[name] == value:
                    continue
                if isinstance(value, (list, tuple)) and hasattr(projected, "setlist"):
                    projected.setlist(key, value)
                else:
                    projected[key] = value
            if args:
                args[0] = projected
            else:
                kwargs["data"] = projected
        super().__init__(*args, **kwargs)
        if adapter:
            # Show the value that renders. Explicit initials take precedence, even when their
            # native value needs no projection.
            projected_explicit = self._project_config(explicit_initial)
            # Only replace stored values that projection changed: django-entangled has already
            # resolved stored model references (e.g. images) to model instances.
            for key, val in self._project_config(stored).items():
                if key in self.fields and key not in projected_explicit:
                    if key not in stored or stored[key] != val:
                        self.initial[key] = val
            for key, val in projected_explicit.items():
                if key in self.fields:
                    self.initial[key] = val
            for name, field in self.fields.items():
                if name in self._project_fields:
                    continue
                try:
                    field.initial = adapter.value(name, field.initial)
                except (ValueError, KeyError, TypeError):
                    pass
                self._offer_initial_choice(name, field)

    def _offer_initial_choice(self, name, field):
        """Let a token choice widget show (and post back) a stored value it does not list,
        so saving an unchanged form keeps it instead of failing or replacing it.

        Only token fields qualify: a stale value of another field (e.g. a removed template)
        must still be rejected. A stored token this adapter cannot express (e.g. surface-3)
        is offered too: posted back unchanged it is kept, and the editor can still replace
        or clear it. Only a newly selected unsupported token is an error.
        """
        if name in tokens.SPACING_FIELDS and isinstance(field, forms.MultiValueField):
            value = self.initial.get(name, field.initial)
            if isinstance(value, str) and value:
                for subfield, widget, part in zip(field.fields, field.widget.widgets, field.widget.decompress(value)):
                    if isinstance(subfield, forms.ChoiceField) and part and not subfield.valid_value(part):
                        subfield.choices = [*subfield.choices, (part, part)]
                        widget.choices = subfield.choices
            return
        if tokens.canonical_key(name) not in tokens.FIELD_VALUES:
            return
        if not isinstance(field, forms.ChoiceField) or isinstance(
            field, (forms.MultipleChoiceField, forms.ModelChoiceField)
        ):
            return
        value = self.initial.get(name, field.initial)
        if value in (None, "") or isinstance(value, (dict, list)) or field.valid_value(value):
            return
        field.choices = [*field.choices, (value, value)]

    @staticmethod
    def _expressible(name, token):
        try:
            settings.token_adapter.value(name, token)
        except (ValueError, KeyError, TypeError):
            return False
        return True

    def _project_config(self, config, *, report_errors=False, stored=None):
        """Project canonical values onto the widgets' native values.

        With ``report_errors``, submitted values that cannot be projected are form errors,
        except a stored token posted back unchanged (see ``_offer_initial_choice``).
        """
        result = {}
        for field, token in config.items():
            if field in self._project_fields:
                result[field] = token
                continue
            try:
                result.update(settings.token_adapter.config_values({field: token}))
            except (ValueError, KeyError, TypeError) as exc:
                editable = self.base_fields.get(field) or self.base_fields.get(tokens.legacy_key(field))
                unchanged = stored is not None and tokens.same_value(stored.get(tokens.canonical_key(field)), token)
                if report_errors and editable is not None and not editable.disabled and not unchanged:
                    self._token_errors.append((tokens.legacy_key(field), f"Invalid {field} token: {exc}"))
                if field in tokens.SPACING_FIELDS and isinstance(token, dict):
                    # Keep a stored non-native size visible in both spacing controls.
                    # This editor representation must not relax render/migration checks.
                    try:
                        token = settings.token_adapter.spacing_widget_value(token)
                    except (ValueError, KeyError, TypeError, AttributeError):
                        pass
                result[tokens.legacy_key(field)] = token
        return result

    def _clean_fields(self):
        # Disabled config fields are read-only storage, including tokens that
        # this adapter cannot express. Do not validate them against widget choices.
        preserved = {}
        if settings.token_adapter:
            for name in self._meta.entangled_fields.get("config", ()):
                field = self.fields.get(name)
                if name in self._project_fields:
                    continue
                key = tokens.canonical_key(name)
                config = self.instance.config or {}
                if field is not None and field.disabled and (key in config or name in config):
                    token = self._explicit_config_initial.get(name, config.get(key, config.get(name)))
                    preserved[name] = (field, token)
        fields = self.fields
        if preserved:
            self.fields = {name: field for name, field in fields.items() if name not in preserved}
        try:
            super()._clean_fields()
        finally:
            self.fields = fields
        for name, (_, token) in preserved.items():
            # Form clean() methods consume widget values. Keep unexpressible
            # stored tokens intact, but project supported read-only values too.
            try:
                self.cleaned_data[name] = settings.token_adapter.value(name, token)
            except (ValueError, KeyError, TypeError):
                self.cleaned_data[name] = token

    def _clean_form(self):
        adapter = settings.token_adapter
        if adapter is None:
            return super()._clean_form()
        original = self.instance.config
        editable_fields = [
            field
            for field in self._meta.entangled_fields.get("config", ())
            if field in self.fields and not self.fields[field].disabled
        ]
        # Errors for fields that are not on this form are not reported: their posted
        # data is ignored, so they can neither be repaired nor block the save.
        for field, message in dict.fromkeys(self._token_errors):
            if field in self.fields and not self.fields[field].disabled:
                self.add_error(field, ValidationError(message))
        canonical = None
        try:
            # The canonical key wins over its legacy alias, as in rendering, so a stored
            # conflict never blocks a save; a submitted field then replaces the value.
            source, _ = tokens.resolve_aliases(original or {}, skip=self._project_fields)
            canonical = tokens.normalize_config(source, skip=self._project_fields)
            # Disabled fields trust server-provided initials, never posted values.
            # Use that source for intent preservation as well as field cleaning.
            for name, token in self._explicit_config_initial.items():
                field = self.fields.get(name)
                if field is not None and field.disabled and name in self._meta.entangled_fields.get("config", ()):
                    key = name if name in self._project_fields else tokens.canonical_key(name)
                    canonical[key] = token if name in self._project_fields else tokens.normalize_value(name, token)
        except ValueError as exc:
            self.add_error(None, ValidationError(str(exc)))
        # django-entangled mutates its input bucket. Give it an isolated, projected
        # dictionary so editing an alias cannot conflict with the previous canonical key.
        projected = self._project_config(canonical) if canonical is not None else {}
        self.instance.config = deepcopy(projected)
        try:
            # Always run the form's clean(), so editors see all errors in one round trip.
            super()._clean_form()
            config = self.cleaned_data.get("config")
            if self._errors:
                self.cleaned_data["config"] = original
            elif config is not None:
                try:
                    normalized = tokens.normalize_config(config, skip=self._project_fields)
                    # Several universal roles share one native recipe (e.g. inverse and
                    # neutral-dark both render as Bootstrap dark). If the widget still posts
                    # the value it was shown, keep the stored role. A deliberate re-selection
                    # of the same native value cannot be told apart and keeps it, too.
                    #
                    # A stored token this adapter cannot express (e.g. surface-3) that is
                    # posted back unchanged is kept and not rejected below.
                    kept = set()
                    for key, stored in canonical.items():
                        name = tokens.legacy_key(key)
                        if key in self._project_fields or name not in projected:
                            continue
                        posted = config.get(name)
                        unchanged = tokens.same_value(posted, projected[name])
                        if unchanged and not self._expressible(name, stored):
                            normalized[key] = stored
                            kept.add(key)
                        elif unchanged and not tokens.same_value(normalized.get(key), stored):
                            normalized[key] = stored
                    # Validate the resulting values, after submitted fields have
                    # replaced invalid stored values. Initial projection errors
                    # must never prevent an editor repairing the configuration.
                    for field in {tokens.canonical_key(field) for field in editable_fields} - kept:
                        if field in normalized and field not in self._project_fields:
                            adapter.value(field, normalized[field])
                    self.cleaned_data["config"] = normalized
                except (ValueError, KeyError, TypeError) as exc:
                    self.add_error(None, ValidationError(str(exc)))
                    self.cleaned_data["config"] = original
        finally:
            self.instance.config = original
