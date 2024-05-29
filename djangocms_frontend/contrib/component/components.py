import importlib

from django import forms
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.models import FrontendUIItem


def _get_mixin_classes(mixins: list, suffix: str = "") -> list[type]:
    """Find and import mixin classes from a list of mixin strings"""
    mixins = [
        (mixin.rsplit(".")[0], f"{mixin.rsplit['.'][-1]}{suffix}Mixin")
        if "." in mixin
        else ("djangocms_frontend.common", f"{mixin}{suffix}Mixin")
        for mixin in mixins
    ]
    return [importlib.import_module(module).__dict__[name] for module, name in mixins]


class CMSFrontendComponent(forms.Form):
    """Base class for frontend components:"""
    @classmethod
    def admin_form_factory(cls, **kwargs) -> type:
        mixins = getattr(cls._component_meta, "mixins", [])
        mixins = _get_mixin_classes(mixins, "Form")
        return type(
            f"{cls.__name__}Form",
            (
                *mixins,
                EntangledModelForm,
                cls,
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
    def plugin_model_factory(cls) -> type:
        model_class = type(
            cls.__name__,
            (FrontendUIItem,),
            {
                "Meta": type(
                    "Meta",
                    (),
                    {
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
        mixins = _get_mixin_classes(mixins)

        return type(
            cls.__name__ + "Plugin",
            (
                *mixins,
                CMSUIPlugin,
            ),
            {
                "name": getattr(cls._component_meta, "name", cls.__name__),
                "module": getattr(cls._component_meta, "module", _("Component")),
                "model": cls.plugin_model_factory(),
                "form": cls.admin_form_factory(),
                "allow_children": getattr(cls._component_meta, "allow_children", False),
                "child_classes": getattr(cls._component_meta, "child_classes", []),
                "render_template": getattr(cls._component_meta, "render_template", CMSUIPlugin.render_template),
                "fieldsets": getattr(cls, "fieldsets", cls._generate_fieldset()),
                "change_form_template": "djangocms_frontend/admin/base.html",
            },
        )

    @classmethod
    @property
    def _component_meta(cls) -> type | None:
        if hasattr(cls, "Meta"):
            return cls.Meta
        return None

    @classmethod
    def _generate_fieldset(cls):
        return [(None, {"fields": cls.declared_fields.keys()})]

    def get_short_description(self) -> str:
        return ""


class Components:
    _registry: dict = {}
    _discovered: bool = False

    def register(self, component):
        self._registry[component.__name__] = (component.plugin_model_factory(), component.plugin_factory())
        return component


components = Components()
if not components._discovered:
    autodiscover_modules("cms_components", register_to=components)
    components._discovered = True
