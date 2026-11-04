import copy
import logging

from cms.models import CMSPlugin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings, tokens
from djangocms_frontend.fields import TagTypeField
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO, PLUGIN_DEFAULTS, SHOW_ADVANCED_SETTINGS

logger = logging.getLogger(__name__)


def normalize_defaults(config, source, skip=()):
    config, conflicts = tokens.resolve_aliases(config, skip=skip)
    for canonical in conflicts:
        legacy = tokens.legacy_key(canonical)
        logger.warning("%s contains conflicting %s and %s; using %s", source, legacy, canonical, canonical)
    return tokens.normalize_config(config, skip=skip)


_plugin_pool = None


def is_plugin_type(name, base):
    """True if the registered plugin ``name`` is the plugin ``base`` or one of its subclasses."""
    global _plugin_pool
    if name == base:
        return True
    if _plugin_pool is None:  # Import once: templates call this for each child plugin.
        from cms.plugin_pool import plugin_pool as _plugin_pool
    try:
        return issubclass(_plugin_pool.get_plugin(name), _plugin_pool.get_plugin(base))
    except KeyError:
        return False


class AbstractFrontendUIItem(CMSPlugin):
    """
    The `AbstractFrontendUIItem` class is an abstract base class that provides common functionality
    for frontend UI items in a CMS plugin. It is a subclass of `CMSPlugin` class.

    Use this class as a base class for custom plugins that add their own database fields.

    Attributes:
        - ui_item: A CharField that represents the UI item name (max length 30).
        - tag_type: A TagTypeField (custom field) that represents the type of HTML tag for the UI item.
        - config: A JSONField that stores additional configuration for the UI item.

    Methods:
        - __init__(*args, **kwargs): Constructor method that initializes the object and sets additional classes.
        - __getattr__(item): Allows properties of the plugin config to be accessed as plugin properties.
        - __str__(): Returns a string representation of the UI item.
        - add_classes(*args): Adds additional classes to the UI item.
        - add_attribute(attr, value=None): Adds an attribute to the configuration attributes.
        - get_attributes(): Returns the attributes as a string for rendering the UI item.
        - save(*args, **kwargs): Saves the UI item to the database.
        - initialize_from_form(form=None): Populates the config JSON field based on initial values from a form.
        - get_short_description(): Returns a plugin-specific short description.
        - framework_info: Returns the framework information for the UI item.

    Note: This is an abstract base class and should not be used directly.
    """

    class Meta:
        abstract = True
        verbose_name = _("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField(blank=True)
    config = models.JSONField(default=dict, encoder=DjangoJSONEncoder)

    def __init__(self, *args, **kwargs):
        self._additional_classes = []
        self.html_id: str | None = None  # HTML id attribute will be set in template tag set_html_id.
        super().__init__(*args, **kwargs)
        if not SHOW_ADVANCED_SETTINGS:
            self.tag_type = getattr(self, "default_tag_type", self._meta.get_field("tag_type").default)

    def __getattr__(self, item):
        """Makes properties of plugin config available as plugin properties.

        A declared entangled field that is not (yet) present in ``config`` resolves to
        its default instead of raising ``AttributeError``. This keeps plugin render code
        (which reads ``instance.<field>`` directly) working for instances that have not
        been through the editing form -- e.g. imported or programmatically built ones --
        while ``clean()`` remains the authoritative place that writes and validates them.
        """
        # 1. Underscore/dunder names are never config fields. Bail first: copy, pickle
        #    and Django internals probe these before ``config`` even exists.
        if item.startswith("_"):
            return super().__getattribute__(item)
        # 2. Read config via __dict__, never self.config -- during unpickle/early init
        #    the field is not set yet and self.config would recurse right here.
        config = self.__dict__.get("config")
        if config is not None and item in config:
            return config[item]
        # 3. Declared entangled field but unset -> its default (a copy, never the shared
        #    cached object). Guarded so resolving the defaults can't re-enter here.
        if not self.__dict__.get("_resolving_defaults"):
            defaults = self._get_config_defaults()
            if item in defaults:
                return copy.deepcopy(defaults[item])
        return super().__getattribute__(item)

    def _get_config_defaults(self):
        """Declared config defaults for this plugin, cached on the (proxy) class.

        The cache is keyed by ``plugin_type``: a registered plugin has its own proxy class
        (one plugin_type), but the base ``FrontendUIItem`` is instantiated directly with
        varying plugin types, so a bare key would leak one plugin's defaults onto another.
        """
        cls = type(self)
        plugin_type = self.__dict__.get("plugin_type")
        cached = vars(cls).get("_config_defaults_cache")
        if cached is not None and cached[0] == plugin_type:
            return cached[1]
        self.__dict__["_resolving_defaults"] = True
        try:
            return self._compute_config_defaults()
        finally:
            self.__dict__.pop("_resolving_defaults", None)

    def _compute_config_defaults(self):
        """Resolve the default value of every declared config field.

        Mirrors ``initialize_from_form``: entangled form-field initials, then model-level
        ``default_config``, then settings ``PLUGIN_DEFAULTS``. Returns a partial (and does
        not cache) when the plugin/form cannot be resolved yet (e.g. no ``plugin_type``).
        """
        cls = type(self)
        defaults = {}
        form = None
        use_tokens = bool(settings.token_adapter)
        if self.__dict__.get("plugin_type"):
            try:
                form = self.get_plugin_class().form
            except Exception:
                form = None
        if form is not None:
            if not getattr(form._meta, "model", None):
                form._meta.model = cls
            try:
                skip = self._token_skip_fields(form) if use_tokens else frozenset()
                bound = form()
                entangled_fields = getattr(form._meta, "entangled_fields", {}).get("config", ())
                for field in entangled_fields:
                    default = self._field_default(bound, field)
                    # Store defaults exactly as ``initialize_from_form`` does, so an instance
                    # completed by ``clean()`` reaches the same canonical config as an edited
                    # one. ``canonical_key``/``normalize_value`` are identities for non-grid
                    # fields, so non-token and project-owned fields are unaffected.
                    if use_tokens and field not in skip:
                        defaults[tokens.canonical_key(field)] = tokens.normalize_value(field, default)
                    else:
                        defaults[field] = default
            except Exception:
                form = None  # incomplete -> don't cache
        for key, value in getattr(cls, "default_config", {}).items():
            defaults[key] = value
        for key, value in PLUGIN_DEFAULTS.get(cls.__name__, {}).items():
            defaults[key] = value
        if form is not None:
            cls._config_defaults_cache = (self.__dict__.get("plugin_type"), defaults)
        return defaults

    @staticmethod
    def _field_default(bound_form, field):
        """Default value stored for an entangled config field.

        Preserves falsey declared initials (``False``, ``0``) -- only ``None`` falls back
        to ``""`` -- so defaults match what a submitted form actually stores.
        """
        if field == "attributes":
            return {}
        initial = bound_form[field].initial
        return "" if initial is None else initial

    @staticmethod
    def _token_skip_fields(form):
        """Fields a project declares itself (never rewritten as tokens). ``form`` may be a
        form class or instance; returns an empty set when tokens are off or unresolvable."""
        if not settings.token_adapter:
            return frozenset()
        from djangocms_frontend.token_forms import project_fields

        form_class = form if isinstance(form, type) else type(form)
        if not hasattr(form_class, "base_fields"):
            return frozenset()
        return project_fields(form_class)

    def __str__(self):
        if "__str__" in self.config:
            return self.config["__str__"]
        return f"{gettext(self.ui_item)} ({str(self.pk)})"

    def add_classes(self, *args):
        for arg in args:
            if arg:
                self._additional_classes += arg.split() if isinstance(arg, str) else arg

    def add_attribute(self, attr, value=None):
        attrs = self.config.get("attributes", {})
        if attr == "style" and attr in attrs:
            value += attrs[attr]
        attrs.update({attr: value})
        self.config["attributes"] = attrs

    def get_attributes(self):
        if SHOW_ADVANCED_SETTINGS:
            attributes = self.config.get("attributes", {})
        else:
            attributes = {}
        classes = self.get_classes()  # get classes
        classes = f'class="{classes}" ' if classes else ""  # to string
        parts = (
            f'{item}="{conditional_escape(value)}"' if value else f"{item}"
            for item, value in attributes.items()
            if item != "class"
        )
        attributes_string = (classes + " ".join(parts)).strip()
        return mark_safe(" " + attributes_string) if attributes_string else ""

    def get_classes(self):
        if SHOW_ADVANCED_SETTINGS:
            attributes = self.config.get("attributes", {})
            classes = set(attributes.get("class", "").split())  # classes added in attriutes
        else:
            classes = set()
        classes.update(self._additional_classes)  # add additional classes
        return conditional_escape(" ".join(classes))

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def clean(self):
        """Ensure every declared config field is present, filling missing ones with their
        default. Runs via ``full_clean()``, so an instance built outside the editing form
        (e.g. an import) reaches the same complete, renderable config as an edited one.

        Fill-missing only: existing (user-set) values are never overwritten, so this is
        idempotent and safe to re-run. When tokens are active the config is normalized to
        canonical storage first, matching ``initialize_from_form``; an unreadable config is
        left untouched (and reported by the form) rather than crashing here.
        """
        super().clean()
        if settings.token_adapter:
            name = self.__class__.__name__
            form = self.get_plugin_class().form if self.__dict__.get("plugin_type") else None
            skip = self._token_skip_fields(form) if form is not None else frozenset()
            try:
                self.config = normalize_defaults(self.config, f"{name} configuration", skip)
            except (ValueError, AttributeError) as exc:
                # Non-object or newer-schema config: leave it for the form to report
                # rather than mixing in defaults written in another schema.
                logger.warning("Cannot clean %s: %s", name, exc)
                return
        for key, value in self._get_config_defaults().items():
            self.config.setdefault(key, copy.deepcopy(value))

    def initialize_from_form(self, form=None):
        """Populates the config JSON field based on initial values provided by the fields of form.
        After setting form defaults, applies per-model defaults from the model's ``default_config``
        class attribute (if any), then from the ``DJANGOCMS_FRONTEND_PLUGIN_DEFAULTS`` setting
        (keyed by model class name). Setting-based defaults take highest priority."""
        if form is None:
            form = self.get_plugin_class().form
        if isinstance(form, type):  # if is class
            if not getattr(form._meta, "model", None):
                form._meta.model = self.__class__
            form = form()  # instantiate
        entangled_fields = getattr(getattr(form, "_meta", None), "entangled_fields", {}).get("config", ())
        defaults = getattr(self, "default_config", {})
        project_defaults = PLUGIN_DEFAULTS.get(self.__class__.__name__, {})
        from djangocms_frontend.token_forms import project_fields

        name = self.__class__.__name__
        use_tokens = bool(settings.token_adapter)
        skip = project_fields(type(form)) if use_tokens and hasattr(form, "base_fields") else frozenset()
        if use_tokens:
            try:
                self.config = normalize_defaults(self.config, f"{name} configuration", skip)
            except ValueError as exc:
                # Leave an unreadable configuration (e.g. a newer schema) untouched
                # rather than mixing in defaults written in another schema.
                logger.warning("Cannot initialize %s: %s", name, exc)
                return self
            sources = []
            default_sources = ((defaults, f"{name}.default_config"), (project_defaults, f"PLUGIN_DEFAULTS[{name}]"))
            for values, source in default_sources:
                try:
                    sources.append(normalize_defaults(values, source, skip))
                except ValueError as exc:
                    # A broken defaults source must not make plugin creation fail.
                    logger.warning("Ignoring %s: %s", source, exc)
                    sources.append({})
            defaults, project_defaults = sources
        for field in entangled_fields:
            initial = self._field_default(form, field)
            if use_tokens and field not in skip:
                self.config.setdefault(tokens.canonical_key(field), tokens.normalize_value(field, initial))
            else:
                self.config.setdefault(field, initial)
        # Apply model-level defaults (override form defaults)
        self.config.update(defaults)
        # Apply settings-level defaults (highest priority)
        self.config.update(project_defaults)
        return self

    def get_framework_value(self, field, default=""):
        """Presentation value for structure-board descriptions and project templates."""
        if settings.token_adapter:
            return settings.token_adapter.field_value(self, field, default)
        return self.config.get(field, default)

    def get_parent_plugin_instance(self, plugin_type=None):
        """Return the concrete parent instance, resolved once per instance. With ``plugin_type``,
        only if the parent's plugin is that plugin or a subclass of it."""
        parent = self.parent
        if parent is None or plugin_type is not None and not is_plugin_type(parent.plugin_type, plugin_type):
            return None
        cached = self.__dict__.get("_framework_parent")
        if cached is None or cached[0] is not parent:
            cached = (parent, parent.get_plugin_instance()[0])
            self._framework_parent = cached
        return cached[1]

    def get_parent_framework_value(self, plugin_type, field):
        """Share parent resolution between render mixins and templates."""
        concrete = self.get_parent_plugin_instance(plugin_type)
        return concrete.get_framework_value(field) if concrete is not None else ""

    def get_short_description(self):
        """Plugin-specific short description (to be defined by subclasses). Try title attribute first."""
        return self.config.get("title", "")

    @property
    def framework_info(self):
        return FRAMEWORK_PLUGIN_INFO.get(self.__class__.__name__, None)


class FrontendUIItem(AbstractFrontendUIItem):
    """

    Class: FrontendUIItem

    Inherits From: AbstractFrontendUIItem

    Description:
    This class represents a UI item in the frontend. It is used to define the behavior and attributes
    of a UI item in the user interface.

    Use this class as a base class for custom plugins that do not add their own database fields but
    use the entangled form fields instead.

    Attributes:
    - verbose_name (str): The verbose name of the UI item.

    Methods:
    None

    """

    class Meta:
        verbose_name = _("UI item")
