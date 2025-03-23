import os
from collections import defaultdict

from django.apps import AppConfig, apps
from django.template import loader

from djangocms_frontend.component_base import CMSFrontendComponent


def find_cms_component_templates() -> list[str]:
    templates = []
    for app in apps.get_app_configs():
        app_template_dir = os.path.join(app.path, "templates", app.label, "cms_components")
        if os.path.exists(app_template_dir):
            for root, _, files in os.walk(app_template_dir):
                for file in files:
                    if file.endswith(".html") or file.endswith(".htm"):
                        relative_path = os.path.relpath(os.path.join(root, file), app_template_dir)
                        templates.append(f"{app.label}/cms_components/{relative_path}")
    return templates


def component_factory(component: tuple, fields: list[tuple], template: str) -> CMSFrontendComponent:
    args, kwargs = component
    (name,) = args

    kwargs["render_template"] = template
    meta = type("Meta", (), kwargs)
    cls = type(
        name,
        (CMSFrontendComponent,),
        {
            "Meta": meta,
            "__module__": "djangocms_frontend.contrib.auto_component.cms_components",
            **{
                # Django template engine instantiates objects -- re-instantiate them here
                args[0]: args[1].__class__(**kwargs)
                for args, kwargs in fields
            },
        },
    )
    return cls


def scan_templates_for_component_declaration(templates: list[str]) -> list[CMSFrontendComponent]:
    from django.forms import fields

    components = []

    for template_name in templates:
        context = {"_cms_components": defaultdict(list), "forms": fields, "instance": {}}
        loader.render_to_string(template_name, context)
        cms_component = context["_cms_components"].get("cms_component", [])
        fields = context["_cms_components"].get("fields", [])
        if len(cms_component) == 1:
            components.append(component_factory(cms_component[0], fields, template_name))
        elif len(cms_component) > 1:
            raise ValueError(f"Multiple cms_component tags found in {template_name}")
    return components


class AutoComponentConfig(AppConfig):
    name = "djangocms_frontend.contrib.auto_component"

    def ready(self):
        from djangocms_frontend.cms_plugins import update_plugin_pool
        from djangocms_frontend.component_pool import components

        templates = find_cms_component_templates()

        auto_components = scan_templates_for_component_declaration(templates)
        for component in auto_components:
            components.register(component)

        update_plugin_pool()
