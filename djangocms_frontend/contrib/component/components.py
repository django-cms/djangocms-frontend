import importlib
import typing
import warnings

from cms.api import add_plugin
from cms.plugin_base import CMSPluginBase
from django import forms
from django.apps import apps
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.models import FrontendUIItem


def _get_mixin_classes(mixins: list, suffix: str = "") -> list[type]:
    """Find and import mixin classes from a list of mixin strings"""
    mixins = [
        (mixin.rsplit(".")[0], f"{mixin.rsplit('.')[-1]}{suffix}Mixin")
        if "." in mixin
        else ("djangocms_frontend.common", f"{mixin}{suffix}Mixin")
        for mixin in mixins
    ]
    return [importlib.import_module(module).__dict__[name] for module, name in mixins]


class CMSFrontendComponent(forms.Form):
    """Base class for frontend components:"""

    slot_template = "djangocms_frontend/slot.html"
    _base_form = EntangledModelForm
    _plugin_mixins = []
    _model_mixins = []

    @classmethod
    def admin_form_factory(cls, **kwargs) -> type:
        mixins = getattr(cls._component_meta, "mixins", [])
        mixins = _get_mixin_classes(mixins, "Form")
        return type(
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

    @classmethod
    def get_slot_plugins(cls) -> dict[str:str]:
        slots : list[tuple[str, str]] = getattr(cls._component_meta, "slots", [])
        return {
            f"{cls.__name__}{slot[0].capitalize()}Plugin": slot[1] for slot in slots
        }

    @classmethod
    def plugin_model_factory(cls) -> type:
        app_config = apps.get_containing_app_config(cls.__module__)
        if app_config is None:
            raise ValueError(f"Cannot find app_config for {cls.__module__}")
        model_class = type(
            cls.__name__,
            (*cls._model_mixins, FrontendUIItem,),
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
                "__module__": "djangocms_frontend.contrib.component.models",
            },
        )
        return model_class

    @classmethod
    def plugin_factory(cls) -> type:
        mixins = getattr(cls._component_meta, "mixins", [])
        slots = cls.get_slot_plugins()
        mixins = _get_mixin_classes(mixins)

        return type(
            cls.__name__ + "Plugin",
            (
                *mixins,
                *cls._plugin_mixins,
                CMSUIPlugin,
            ),
            {
                "name": getattr(cls._component_meta, "name", cls.__name__),
                "module": getattr(cls._component_meta, "module", _("Component")),
                "model": cls.plugin_model_factory(),
                "form": cls.admin_form_factory(),
                "allow_children": getattr(cls._component_meta, "allow_children", False) or slots,
                "child_classes": getattr(cls._component_meta, "child_classes", []) + list(slots.keys()),
                "render_template": getattr(cls._component_meta, "render_template", CMSUIPlugin.render_template),
                "fieldsets": getattr(cls, "fieldsets", cls._generate_fieldset()),
                "change_form_template": "djangocms_frontend/admin/base.html",
                "slots": slots,
                "save_model": cls.save_model,
                "link_fieldset_position": getattr(cls._component_meta, "link_fieldset_position", 1),
            },
        )

    @classmethod
    def slot_plugin_factory(cls) -> list[type]:
        slots = cls.get_slot_plugins()
        return [
            type(
                slot,
                (CMSPluginBase,),
                {
                    "name": slot_name,
                    "module": getattr(cls._component_meta, "module", _("Component")),
                    "allow_children": True,
                    "parent_classes": cls.__name__ + "Plugin",
                    "render_template": cls.slot_template,
                },
            )
            for slot, slot_name in slots.items()
        ]

    @classmethod
    def get_registration(cls) -> tuple[type, type, list[type]]:
        return (
            cls.plugin_model_factory(),
            cls.plugin_factory(),
            cls.slot_plugin_factory(),
        )

    @classmethod
    @property
    def _component_meta(cls) -> typing.Optional[type]:
        if hasattr(cls, "Meta"):
            return cls.Meta
        return None

    @classmethod
    def _generate_fieldset(cls) -> list[tuple[typing.Optional[str], dict]]:
        return [(None, {"fields": cls.declared_fields.keys()})]

    def get_short_description(self) -> str:
        return ""

    def save_model(self, request, obj, form: forms.Form, change: bool) -> None:
        """Auto-createas slot plugins upon creation of component plugin instance"""
        super(CMSUIPlugin, self).save_model(request, obj, form, change)
        if not change:
            for slot in self.slots.keys():
                add_plugin(obj.placeholder, slot, obj.language, target=obj)


class ComponentLinkMixin:
    from djangocms_frontend.contrib.link.cms_plugins import LinkPluginMixin
    from djangocms_frontend.contrib.link.forms import AbstractLinkForm
    from djangocms_frontend.contrib.link.models import GetLinkMixin

    _base_form = AbstractLinkForm
    _model_mixins = [GetLinkMixin]
    _plugin_mixins = [LinkPluginMixin]


class Components:
    _registry: dict = {}
    _discovered: bool = False

    def register(self, component):
        if component.__name__ in self._registry:
            warnings.warn(f"Component {component.__name__} already registered", stacklevel=2)
            return component
        self._registry[component.__name__] = component.get_registration()
        return component


components = Components()
if not components._discovered:
    autodiscover_modules("cms_components", register_to=components)
    components._discovered = True
