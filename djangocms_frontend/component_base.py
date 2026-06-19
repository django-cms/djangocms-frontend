import importlib

from cms import __version__ as cms_version
from cms.models import CMSPlugin
from django import forms
from django.apps import apps
from django.forms.forms import DeclarativeFieldsMetaclass
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

# django CMS 5.1+ understands ``child_classes = "auto"`` to auto-detect which
# plugins may be nested. On older versions ``child_classes`` is treated as a
# membership test, so the sentinel must not be emitted there.
_cms_major_minor = tuple(int(part) for part in cms_version.split(".")[:2] if part.isdigit())
_CMS_AUTO_CHILD_CLASSES = _cms_major_minor >= (5, 1)


def _import_or_empty(module, name):
    try:
        return importlib.import_module(module).__dict__[name]
    except (ImportError, KeyError):
        return type(name, (), {})


def _get_mixin_classes(mixins: list, suffix: str = "") -> list[type]:
    """Find and import mixin classes from a list of mixin strings"""
    mixins = [
        (mixin.rsplit(".")[0], f"{mixin.rsplit('.')[-1]}{suffix}Mixin")
        if "." in mixin
        else ("djangocms_frontend.common", f"{mixin}{suffix}Mixin")
        for mixin in reversed(mixins)
    ]

    return [_import_or_empty(module, name) for module, name in mixins]


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, owner):
        return self.fget(owner)


class Slot:
    """Slot class as syntactic surgar to more easily define slot plugins"""

    def __init__(self, name, verbose_name, **kwargs):
        self.name = name
        self.verbose_name = verbose_name
        self.kwargs = kwargs


class SlotModel(CMSPlugin):
    class Meta:
        proxy = True

    def get_short_description(self):
        return format_html("<b>{}</b>", _("Slot"))


def _component_qualname_parts(qualname: str) -> list[str]:
    """Return the chain of lexically-nesting class names, ignoring any enclosing
    function scope (e.g. ``Outer.test.<locals>.Tab.Item`` -> ``["Tab", "Item"]``)."""
    parts = qualname.split(".")
    if "<locals>" in parts:
        # Keep only the class names that follow the innermost function scope
        parts = parts[len(parts) - parts[::-1].index("<locals>") :]
    return parts


def _ensure_own_meta(cls) -> type:
    """Return the component's *own* ``Meta`` class, creating one (inheriting any
    ``Meta`` defined further up) if the component does not declare its own."""
    if "Meta" in cls.__dict__:
        return cls.__dict__["Meta"]
    base = getattr(cls, "Meta", None)
    meta = type("Meta", (base,) if base else (), {})
    cls.Meta = meta
    return meta


def _insert_template_folder(path: str, template: str) -> str:
    """Insert ``template`` as a folder right before the file name of ``path``,
    e.g. ``xy/content.html`` + ``pills`` -> ``xy/pills/content.html``."""
    head, sep, tail = path.rpartition("/")
    return f"{head}/{template}/{tail}" if sep else f"{template}/{tail}"


def _resolve_template(instance) -> str:
    """Return the selected template string for ``instance``.

    A component that declares a ``template`` field owns its choice. One that does
    not inherits from the nearest ancestor that *declares* a ``template`` field
    (its template owner). The walk stops at that owner even if its value is empty
    -- so a tab item never reaches past its tab to a grandparent that happens to
    have its own, unrelated ``template``."""
    node = instance
    while node is not None:
        if getattr(node, "_has_template_field", False):
            config = getattr(node, "config", None)
            return config.get("template", "") if isinstance(config, dict) else ""
        parent = getattr(node, "parent", None)
        if parent is None:
            break
        node = parent.get_plugin_instance()[0]
    return ""


class ComponentMeta(DeclarativeFieldsMetaclass):
    """Metaclass that wires up nested ``CMSFrontendComponent`` declarations.

    A component declared inside another component becomes a child plugin of the
    outer one. Its name is qualified with the parent's (``Tab.Item`` ->
    ``TabItem`` / ``TabItemPlugin``) and the parent/child relationship is filled
    in automatically: ``parent_classes`` and ``require_parent`` on the child,
    ``child_classes`` and ``allow_children`` on the parent. Explicit ``Meta``
    values always take precedence.
    """

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        if not any(isinstance(base, ComponentMeta) for base in bases):
            # The ``CMSFrontendComponent`` base class itself - nothing to wire.
            return cls

        qualname = namespace.get("__qualname__", name)
        parts = _component_qualname_parts(qualname)

        # A nested component is qualified with its parent's name: Tab.Item -> TabItem
        if len(parts) > 1:
            cls.__name__ = "".join(parts)
            parent_plugin = "".join(parts[:-1]) + "Plugin"
            meta = _ensure_own_meta(cls)
            if not hasattr(meta, "parent_classes"):
                meta.parent_classes = [parent_plugin]
            if not hasattr(meta, "require_parent"):
                meta.require_parent = True

        # Adopt directly-nested components as child plugins of this component.
        # The nested children are wired up via their own ``parent_classes`` (set
        # above); the parent only needs to allow children. Which children are
        # permitted is resolved in ``_get_child_classes`` ("auto" on django CMS
        # 5.1+, an explicit enumeration before that).
        nested = [
            value
            for value in namespace.values()
            if isinstance(value, ComponentMeta) and value.__qualname__.rsplit(".", 1)[0] == qualname
        ]
        cls._nested_components = nested
        if nested:
            meta = _ensure_own_meta(cls)
            if not hasattr(meta, "allow_children"):
                meta.allow_children = True
        return cls


class CMSFrontendComponent(forms.Form, metaclass=ComponentMeta):
    """Base class for frontend components:"""

    slot_template = "djangocms_frontend/slot.html"
    _base_form = EntangledModelForm
    _plugin_mixins = []
    _model_mixins = []
    _admin_form = None
    _model = None
    _plugin = None
    _nested_components = []
    META_FIELDS = [
        "is_local",
        "is_slot",
        "disable_edit",
        "disable_child_plugins",
        "show_add_form",
        "frontend_editable_fields",
        "link_fieldset_position",
        "require_parent",
        "parent_classes",
        "allowed_models",
    ]

    @classmethod
    def admin_form_factory(cls, **kwargs) -> type:
        if cls._admin_form is None:
            from djangocms_frontend.fields import TemplateChoiceMixin
            from djangocms_frontend.models import FrontendUIItem

            mixins = getattr(cls._component_meta, "mixins", [])
            mixins = _get_mixin_classes(mixins, "Form")
            # The component carries ``ComponentMeta`` while the base form carries
            # entangled/model-form metaclasses (siblings under Django's
            # ``DeclarativeFieldsMetaclass``). Build a combined metaclass so the
            # generated form has a single, consistent one.
            form_metaclass = type(cls._base_form)
            if not issubclass(form_metaclass, ComponentMeta):
                try:
                    form_metaclass = type(
                        f"{cls.__name__}FormMeta",
                        (ComponentMeta, form_metaclass),
                        {},
                    )
                except TypeError as exc:  # pragma: no cover - defensive
                    raise TypeError(
                        f"Cannot build the admin form for component {cls.__name__!r}: its base form "
                        f"{cls._base_form.__name__!r} uses a metaclass incompatible with ComponentMeta. "
                        f"Provide a compatible '_base_form'."
                    ) from exc
            cls._admin_form = form_metaclass(
                f"{cls.__name__}Form",
                (
                    # Hides the template field when only one choice is available;
                    # a no-op for components without a `template` field.
                    TemplateChoiceMixin,
                    *mixins,
                    cls,
                    cls._base_form,
                ),
                {
                    **kwargs,
                    "Meta": type(
                        "Meta",
                        (),
                        {
                            "model": FrontendUIItem,
                            "entangled_fields": {
                                "config": list(cls.declared_fields.keys()),
                            },
                        },
                    ),
                },
            )
        return cls._admin_form

    @classmethod
    def get_slot_plugins(cls) -> dict[str:str]:
        slots: list[Slot] = [
            slot if isinstance(slot, Slot) else Slot(*slot) for slot in getattr(cls._component_meta, "slots", [])
        ]
        return {f"{cls.__name__}{slot.name.capitalize()}Plugin": slot for slot in slots}

    @classmethod
    def plugin_model_factory(cls) -> type:
        if cls._model is None:
            from djangocms_frontend.models import FrontendUIItem

            app_config = apps.get_containing_app_config(cls.__module__)
            if app_config is None:  # pragma: no cover
                raise ValueError(f"Cannot find app_config for {cls.__module__}")
            model_attrs = {
                "Meta": type(
                    "Meta",
                    (),
                    {
                        "app_label": app_config.label,
                        "proxy": True,
                        "managed": False,
                        "verbose_name": getattr(cls._component_meta, "name", cls.__name__),
                    },
                ),
                "get_short_description": cls.get_short_description,
                "__module__": cls.__module__,
                # Lets ``_resolve_template`` find the template-owning ancestor.
                "_has_template_field": "template" in cls.declared_fields,
            }
            default_config = getattr(cls._component_meta, "default_config", None)
            if default_config:
                model_attrs["default_config"] = default_config
            cls._model = type(
                cls.__name__,
                (
                    *cls._model_mixins,
                    FrontendUIItem,
                ),
                model_attrs,
            )
        return cls._model

    @classmethod
    def _get_child_classes(cls, slots: dict) -> list | str | None:
        """Resolve the plugin's ``child_classes``.

        An explicit ``Meta.child_classes`` always wins and is extended with the
        component's slots. When the component has nested components and/or slots
        but no explicit list, django CMS 5.1+ uses ``"auto"``: the allowed
        children are resolved from the plugins that name this one in their
        ``parent_classes``, so the parent makes no assumptions about them. Before
        5.1 ``"auto"`` is unavailable, so those children are enumerated instead.

        A plain ``allow_children`` component (no nested, no slots) returns
        ``None`` -- django CMS reads that as "unrestricted". (An explicit empty
        ``[]`` means "no children allowed", so it is left untouched.)
        """
        slot_classes = list(slots.keys())
        child_classes = getattr(cls._component_meta, "child_classes", None)
        if child_classes == "auto":
            return "auto"
        if child_classes is not None:
            return list(child_classes) + slot_classes
        if cls._nested_components or slot_classes:
            if _CMS_AUTO_CHILD_CLASSES:
                return "auto"
            # Older django CMS: enumerate nested components and slots explicitly.
            nested_classes = [f"{component.__name__}Plugin" for component in cls._nested_components]
            return nested_classes + slot_classes
        return None

    @classmethod
    def plugin_factory(cls) -> type:
        from .ui_plugin_base import CMSUIComponent

        if cls._plugin is None:
            mixins = getattr(cls._component_meta, "mixins", [])
            slots = cls.get_slot_plugins()
            mixins = _get_mixin_classes(mixins)

            allow_children = slots or getattr(cls._component_meta, "allow_children", False)
            child_classes = cls._get_child_classes(slots)

            cls._plugin = type(
                cls.__name__ + "Plugin",
                (
                    *mixins,
                    *cls._plugin_mixins,
                    CMSUIComponent,
                ),
                {
                    "name": getattr(cls._component_meta, "name", cls.__name__),
                    "module": getattr(cls._component_meta, "module", _("Components")),
                    "model": cls.plugin_model_factory(),
                    "form": cls.admin_form_factory(),
                    "allow_children": allow_children,
                    "child_classes": child_classes,
                    "render_template": getattr(cls._component_meta, "render_template", CMSUIComponent.render_template),
                    "fieldsets": getattr(cls._component_meta, "fieldsets", cls._generate_fieldset()),
                    "change_form_template": getattr(
                        cls._component_meta, "change_form_template", "djangocms_frontend/admin/base.html"
                    ),
                    "slots": slots,
                    "save_model": cls.save_model,
                    # Default template resolution (insert selected template folder
                    # before the file name); a component-defined override wins.
                    "get_render_template": cls.get_render_template,
                    **{
                        field: getattr(cls._component_meta, field)
                        for field in cls.META_FIELDS
                        if hasattr(cls._component_meta, field)
                    },
                    **(
                        {
                            "get_render_template": cls.get_render_template,
                            "TEMPLATES": getattr(cls, "TEMPLATES", (("default", "Default"),)),
                        }
                        if hasattr(cls, "get_render_template")
                        else {}
                    ),
                    "__module__": "djangocms_frontend.cms_plugins",
                },
            )
        return cls._plugin

    @classmethod
    def slot_plugin_factory(cls) -> list[type]:
        from cms.plugin_base import CMSPluginBase

        slots = cls.get_slot_plugins()
        return [
            type(
                name,
                (CMSPluginBase,),
                {
                    "name": force_str(slot.verbose_name),
                    "module": getattr(cls._component_meta, "module", _("Component")),
                    "allow_children": True,
                    "edit_disabled": True,
                    "is_local": False,
                    "is_slot": True,
                    "show_add_form": False,
                    "parent_classes": [cls.__name__ + "Plugin"],
                    "render_template": cls.slot_template,
                    "model": SlotModel if _cms_major_minor >= (5, 0) else CMSPlugin,
                    **slot.kwargs,
                },
            )
            for name, slot in slots.items()
        ]

    @classmethod
    def get_registration(cls) -> tuple[type, type, list[type]]:
        return (
            cls.plugin_model_factory(),
            cls.plugin_factory(),
            cls.slot_plugin_factory(),
        )

    @classproperty
    def _component_meta(cls) -> type | None:
        return getattr(cls, "Meta", None)

    @classmethod
    def _generate_fieldset(cls) -> list[tuple[str | None, dict]]:
        return [(None, {"fields": cls.declared_fields.keys()})]

    def get_render_template(self, context, instance, placeholder):
        """Default render template resolution for components.

        When a ``template`` is selected, it is inserted as a folder right before
        the file name of the plugin's ``render_template``, e.g.
        ``xy/content.html`` -> ``xy/<template>/content.html``. The template is
        taken from the plugin's own config or, if it has none, from the nearest
        ancestor plugin that does -- so child components follow their parent's
        template choice. Falls back to the bare ``render_template`` when no
        template is selected or the resolved template does not exist.

        Note: ``self`` is the plugin instance this method is attached to.
        """
        template = _resolve_template(instance)
        render_template = self.render_template
        if template:
            candidate = _insert_template_folder(render_template, template)
            try:
                select_template([candidate])
                return candidate
            except TemplateDoesNotExist:
                pass
        return render_template

    def get_short_description(self) -> str:
        return self.config.get("title", "")

    def save_model(self, request, obj, form: forms.Form, change: bool) -> None:
        """Auto-creates slot plugins upon creation of component plugin instance"""
        from cms.api import add_plugin

        from .ui_plugin_base import CMSUIComponent

        super(CMSUIComponent, self).save_model(request, obj, form, change)
        if not change:
            for slot in self.slots.keys():
                add_plugin(obj.placeholder, slot, obj.language, target=obj)
