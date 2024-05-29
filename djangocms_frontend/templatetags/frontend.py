import json

from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import AsTag
from cms.templatetags.cms_tags import render_plugin
from django import template
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import safe
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.html import conditional_escape, mark_safe

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.fields import HTMLsanitized
from djangocms_frontend.helpers import get_related_object as related_object
from djangocms_frontend.pool import plugin_tag_pool

register = template.Library()


@register.simple_tag
def get_attributes(attribute_field, *add_classes):
    """Joins a list of classes with an attributes field and returns all html attributes"""
    additional_classes = set()
    for classes in add_classes:
        if classes:
            additional_classes.update(classes.split() if isinstance(classes, str) else classes)
    attrs = []
    if attribute_field:
        for key, val in attribute_field.items():
            if key.lower() == "class":
                val = " ".join(additional_classes.union(set(val.split())))
            if val:
                attrs.append(f'{key}="{conditional_escape(val)}"')
            else:
                attrs.append(f"{key}")
    if additional_classes and (not attribute_field or "class" not in attribute_field):
        attrs.append(f'class="{conditional_escape(" ".join(additional_classes))}"')
    return mark_safe(" ".join(attrs))


@register.filter
def get_related_object(reference):
    return related_object(dict(obj=reference), "obj")


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


@register.filter
def json_dumps(data):
    """Converts data to JSON forcing text on lazy gettext translation"""
    return mark_safe(json.dumps(data, cls=LazyEncoder))


@register.filter
def html_safe(data):
    if HTMLsanitized:
        return safe(data)
    return data


@register.filter
def safe_caption(data):
    if data[:3] == "<p>" and data[-4:] == "</p>":
        block = data[3:-4]
        if "<p>" not in block:
            data = block
    if HTMLsanitized:
        return safe(data)
    return data


@register.simple_tag(takes_context=True)
def framework_info(context, item, as_json=True):
    """Retrieves framework_info for plugin either from existing plugin or from
    content type"""
    plugin = context.get("plugin", None)
    if plugin:  # if possible get from plugin
        return (
            mark_safe(json.dumps(plugin.framework_info.get(item, ""), cls=LazyEncoder))
            if as_json
            else plugin.get(item, "")
        )
    framework_info = context.get("framework_info", {})  # already available
    if not framework_info:
        content_type_id = context.get("content_type_id", None)
        if content_type_id:  # Get from content_type
            model_name = ContentType.objects.get(id=content_type_id).model_class().__name__
            framework_info = settings.FRAMEWORK_PLUGIN_INFO.get(model_name, {})
            context["framework_info"] = framework_info  # and store
    return (
        mark_safe(json.dumps(framework_info.get(item, ""), cls=LazyEncoder))
        if as_json
        else framework_info.get(item, "")
    )


@register.inclusion_tag("djangocms_frontend/user_message.html", takes_context=True)
def user_message(context, message):
    """Renders a user message"""
    toolbar = getattr(context.get("request", None), "toolbar", None)
    if settings.SHOW_EMPTY_CHILDREN and toolbar.edit_mode_active:
        return {"message": message}
    return {}


class DummyPlugin:
    def __init__(self, nodelist):
        self.nodelist = nodelist
        super().__init__()


class Plugin(AsTag):
    name = "plugin"
    options = Options(
        Argument("name", required=True),
        MultiKeywordArgument("kwargs", required=False),
        "as",
        Argument("varname", resolve=False, required=False),
        blocks=[("endplugin", "nodelist")],
    )

    def message(self, message):
        return f"<!-- {message} -->" if django_settings.DEBUG else ""

    def get_value(self, context, name, kwargs, nodelist):
        if name not in plugin_tag_pool:
            return self.message(f"Plugin \"{name}\" not found in pool for plugins usable with {{% plugin %}}")
        context.push()
        instance = (plugin_tag_pool[name]["defaults"])
        plugin_class = plugin_tag_pool[name]["class"]
        if issubclass(plugin_class, CMSUIPlugin):
            #
            instance["config"].update(kwargs)
        else:
            instance.update(kwargs)
        # Create context
        context["instance"] = plugin_class.model(**instance)
        # Call render method of plugin
        context = plugin_class().render(context, context["instance"], None)
        # Replace inner plugins with the nodelist, i.e. the content within the plugin tag
        context["instance"].child_plugin_instances = [DummyPlugin(nodelist)]
        # ... and redner
        result = plugin_tag_pool[name]["template"].render(context.flatten())
        context.pop()
        return result


register.tag(Plugin.name, Plugin)


@register.simple_tag(takes_context=True)
def render_child_plugins(context, instance, plugin_type=None):
    """Renders the child plugins of a plugin instance"""
    if not instance.child_plugin_instances:
        return ""
    context.push()
    context["parent"] = instance
    result = ""
    for child in instance.child_plugin_instances:
        if isinstance(child, DummyPlugin):
            result += child.nodelist.render(context)
        else:
            if plugin_type and child.plugin_type == plugin_type:
                result += render_plugin(context, child)
    context.pop()
    return result if result else getattr(instance, "simple_content", "")
