from __future__ import annotations

import copy
import importlib
import warnings

from cms.plugin_pool import plugin_pool
from cms.templatetags.cms_tags import render_plugin
from django.conf import settings
from django.contrib.admin.sites import site as admin_site
from django.template import engines
from django.template.library import SimpleNode
from django.template.loader import get_template

django_engine = engines["django"]

plugin_tag_pool = {}


IGNORED_FIELDS = (
    "id",
    "cmsplugin_ptr",
    "language",
    "plugin_type",
    "position",
    "creation_date",
    "ui_item",
)


def _get_plugindefaults(instance):
    defaults = {
        field.name: getattr(instance, field.name)
        for field in instance._meta.fields
        if field.name not in IGNORED_FIELDS and bool(getattr(instance, field.name))
    }
    defaults["plugin_type"] = instance.__class__.__name__
    return defaults


class _DummyUser:
    is_superuser = True
    is_staff = True


class _DummyRequest:
    user = _DummyUser()


def render_dummy_plugin(context, dummy_plugin):
    return dummy_plugin.nodelist.render(context)


def patch_template(template):
    """Patches the template to use the dummy plugin renderer instead of the real one."""
    copied_template = copy.deepcopy(template)
    patch = False
    for node in copied_template.template.nodelist.get_nodes_by_type(SimpleNode):
        if node.func == render_plugin:
            patch = True
            node.func = render_dummy_plugin
    return copied_template if patch else template


def get_plugin_class(settings_string: str | type) -> type:
    """Get the plugin class from the settings string or import it if it's a dotted path."""
    if isinstance(settings_string, str):
        if "." in settings_string:
            # import the class if a dotted path is given - raise can exception if not found
            module_name, class_name = settings_string.rsplit(".", 1)
            return getattr(importlib.import_module(module_name), class_name)
        # Get the plugin class from the plugin pool by its name
        return plugin_pool.get_plugin(settings_string)
    return settings_string


def setup():
    allowed_plugin_types = tuple(get_plugin_class(cls) for cls in getattr(settings, "CMS_COMPONENT_PLUGINS", []))

    for plugin in plugin_pool.plugins.values():  # We'll check all plugins irrespectivly of placeholder config
        if not issubclass(plugin, allowed_plugin_types):
            continue
        tag_name = plugin.__name__.lower()
        if tag_name.endswith("plugin"):
            tag_name = tag_name[:-6]
        try:
            instance = plugin.model()  # Create instance with defaults
            plugin_admin = plugin(admin_site=admin_site)
            if hasattr(instance, "initialize_from_form"):
                instance.initialize_from_form(plugin.form)
            if tag_name not in plugin_tag_pool:
                template = get_template(plugin_admin._get_render_template({"request": None}, instance, None))
                plugin_tag_pool[tag_name] = {
                    "defaults": {
                        **_get_plugindefaults(instance),
                        **dict(plugin_type=plugin.__name__),
                    },
                    "template": patch_template(template),
                    "class": plugin,
                }
            else:  # pragma: no cover
                warnings.warn(
                    f'Duplicate candidates for {{% plugin "{tag_name}" %}} found. '
                    f"Only registered {plugin_tag_pool[tag_name]['class'].__name__}.",
                    stacklevel=1,
                )
        except Exception as exc:  # pragma: no cover
            warnings.warn(f"{plugin.__name__}: \n{str(exc)}", stacklevel=1)
