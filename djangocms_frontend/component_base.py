import importlib

from django import forms
from django.apps import apps
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm


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
    """Slat class as syntactic surgar to more easily define slot plugins"""

    def __init__(self, name, verbose_name, **kwargs):
        self.name = name
        self.verbose_name = verbose_name
        self.kwargs = kwargs


class CMSFrontendComponent(forms.Form):
    """Base class for frontend components:"""

    slot_template = "djangocms_frontend/slot.html"
    _base_form = EntangledModelForm
    _plugin_mixins = []
    _model_mixins = []
    _admin_form = None
    _model = None
    _plugin = None
    META_FIELDS = [
        "is_local",
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
            from djangocms_frontend.models import FrontendUIItem

            mixins = getattr(cls._component_meta, "mixins", [])
            mixins = _get_mixin_classes(mixins, "Form")
            cls._admin_form = type(
                f"{cls.__name__}Form",
                (
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
            cls._model = type(
                cls.__name__,
                (
                    *cls._model_mixins,
                    FrontendUIItem,
                ),
                {
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
                },
            )
        return cls._model

    @classmethod
    def plugin_factory(cls) -> type:
        from .ui_plugin_base import CMSUIComponent

        if cls._plugin is None:
            mixins = getattr(cls._component_meta, "mixins", [])
            slots = cls.get_slot_plugins()
            mixins = _get_mixin_classes(mixins)

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
                    "allow_children": slots or getattr(cls._component_meta, "allow_children", False),
                    "child_classes": getattr(cls._component_meta, "child_classes", []) + list(slots.keys()),
                    "render_template": getattr(cls._component_meta, "render_template", CMSUIComponent.render_template),
                    "fieldsets": getattr(cls, "fieldsets", cls._generate_fieldset()),
                    "change_form_template": "djangocms_frontend/admin/base.html",
                    "slots": slots,
                    "save_model": cls.save_model,
                    **{
                        field: getattr(cls._component_meta, field)
                        for field in cls.META_FIELDS
                        if hasattr(cls._component_meta, field)
                    },
                    **(
                        {
                            "get_render_template": cls.get_render_template,
                            "TEMPLATES": cls.TEMPLATES,
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
                    "show_add_form": False,
                    "parent_classes": [cls.__name__ + "Plugin"],
                    "render_template": cls.slot_template,
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
