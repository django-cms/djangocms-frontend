import importlib
import os
import warnings
from collections import defaultdict
from collections.abc import Iterator

from django import forms
from django.apps import apps
from django.template.loader import get_template
from django.utils.module_loading import autodiscover_modules
from sekizai.context import SekizaiContext

from djangocms_frontend import settings
from djangocms_frontend.component_base import CMSFrontendComponent


def find_cms_component_templates(subfolder: str) -> list[tuple[str, str]]:
    templates = []
    for app in apps.get_app_configs():
        app_template_dir = os.path.join(app.path, "templates", app.label, subfolder)
        if os.path.exists(app_template_dir):
            for root, _, files in os.walk(app_template_dir):
                for file in files:
                    if file.endswith(".html") or file.endswith(".htm"):
                        relative_path = os.path.relpath(os.path.join(root, file), app_template_dir)
                        templates.append((app.module.__name__, f"{app.label}/{subfolder}/{relative_path}"))
    return templates


class CMSAutoComponentDiscovery:
    default_field_context = {
        "djangocms_text": "djangocms_text.fields.HTMLFormField",
        "djangocms_text_ckeditor": "djangocms_text_ckeditor.fields.HTMLFormField",
        "djangocms_link": "djangocms_link.fields.LinkFormField",
        "djangocms_frontend": [
            "djangocms_frontend.contrib.image.fields.ImageFormField",
            "djangocms_frontend.contrib.icon.fields.IconPickerField",
            "djangocms_frontend.fields.AttributesFormField",
            "djangocms_frontend.fields.ChoicesFormField",
        ],
    }

    def __init__(self, register_to):
        self.default_field_context.update(settings.COMPONENT_FIELDS)
        templates = find_cms_component_templates(settings.COMPONENT_FOLDER)
        auto_components = self.scan_templates_for_component_declaration(templates)
        for component in auto_components:
            register_to.register(component)

    def get_field_context(self) -> dict:
        field_context = {}
        for key, value in self.default_field_context.items():
            if apps.is_installed(key):
                if not isinstance(value, list):
                    value = [value]
                for field in value:
                    if "." in field:
                        module, field_name = field.rsplit(".", 1)
                        field_context[field_name] = importlib.import_module(module).__dict__[field_name]
            elif key not in ("djangocms_text", "djangocms_text_ckeditor"):
                warnings.warn(f"App {key} not installed, skipping field registration", stacklevel=2)
        return field_context

    @staticmethod
    def component_factory(module, component: tuple, fields: list[tuple], template: str) -> CMSFrontendComponent:
        args, kwargs = component
        (name,) = args

        kwargs["render_template"] = template
        meta = type("Meta", (), kwargs)
        return type(
            name,
            (CMSFrontendComponent,),
            {
                "Meta": meta,
                "__module__": module,
                **{
                    # Django template engine instantiates objects -- re-instantiate them here
                    args[0]: args[1].__class__(**kwargs)
                    for args, kwargs in fields
                    if isinstance(args[1], forms.Field)
                },
            },
        )

    def scan_templates_for_component_declaration(
        self, templates: list[tuple[str, str]]
    ) -> Iterator[CMSFrontendComponent]:
        from django.forms import fields

        field_context = self.get_field_context()
        for module, template_name in templates:
            # Create a new context for each template
            context = SekizaiContext(
                {"_cms_components": defaultdict(list), "forms": fields, "instance": {}, **field_context}
            )
            try:
                template = get_template(template_name)
                template.template.render(context)
                cms_component = context["_cms_components"].get("cms_component", [])
                discovered_fields = context["_cms_components"].get("fields", [])
                if len(cms_component) == 1:
                    yield self.component_factory(module, cms_component[0], discovered_fields, template_name)
                elif len(cms_component) > 1:  # pragma: no cover
                    raise ValueError(f"Multiple cms_component tags found in {template_name}")
            except Exception:  # pragma: no cover
                # Skip all templates that do not render
                import logging

                logger = logging.getLogger(__name__)
                logger.error(
                    f"Error rendering template {template_name} to scan for cms frontend components", exc_info=True
                )


class Components:
    _registry: dict = {}
    _discovered: bool = False

    def register(self, component):
        if component.__name__ in self._registry:  # pragma: no cover
            warnings.warn(f"Component {component.__name__} already registered", stacklevel=2)
            return component
        self._registry[component.__name__] = component.get_registration()
        return component

    def __getitem__(self, item):
        return self._registry[item]


components = Components()


def setup():
    if not components._discovered:
        from .cms_plugins import update_plugin_pool

        # First discover components in cms_components module
        autodiscover_modules("cms_components", register_to=components)
        # The discover auto components by their templates
        CMSAutoComponentDiscovery(register_to=components)
        update_plugin_pool()
        components._discovered = True

        if apps.is_installed("djangocms_text"):
            # Hack - update inline editable fields in case djangocms_text is installed
            # BEFORE djangocms_frontend in INSTALLED_APPS:
            # Need to initialize inline fields again to reflect inline fields of the just discovered components
            from djangocms_text.apps import discover_inline_editable_models

            text_config = apps.get_app_config("djangocms_text")
            text_config.inline_models = discover_inline_editable_models()
