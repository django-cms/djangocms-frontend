import json
import typing

from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options, Tag
from classytags.helpers import AsTag
from cms.models import CMSPlugin
from cms.templatetags.cms_tags import CMSEditableObject, render_plugin
from django import template
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.template.defaultfilters import safe
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.html import conditional_escape, mark_safe
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import HTMLsanitized
from djangocms_frontend.helpers import get_related_object as related_object

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


@register.tag
class SlotTag(Tag):
    name = "slot"
    options = Options(
        Argument("slot_name", required=True),
        blocks=[("endslot", "nodelist")],
    )

    def render_tag(self, context, slot_name, nodelist):
        return ""


class DummyPlugin:
    def __init__(self, nodelist, plugin_type, slot_name: typing.Optional[str] = None) -> "DummyPlugin":
        self.nodelist = nodelist
        self.plugin_type = (f"{plugin_type}{slot_name.capitalize()}Plugin") if slot_name else "DummyPlugin"
        if slot_name is None:
            self.parse_slots(nodelist, plugin_type)
        super().__init__()

    def parse_slots(self, nodelist, plugin_type):
        self.slots = [self]
        for node in nodelist:
            if isinstance(node, SlotTag):
                self.slots.append(DummyPlugin(node.nodelist, plugin_type, node.kwargs.get("slot_name")))

    def get_instances(self):
        return self.slots


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
        from djangocms_frontend.plugin_tag import plugin_tag_pool

        if name not in plugin_tag_pool:
            return self.message(f'Plugin "{name}" not found in pool for plugins usable with {{% plugin %}}')
        context.push()
        instance = plugin_tag_pool[name]["defaults"]
        plugin_class = plugin_tag_pool[name]["class"]

        if issubclass(plugin_class.form, EntangledModelFormMixin):
            # Handle entangled forms such as djangocms-frontend's correctly
            for field, value in kwargs.items():
                for container, fields in plugin_class.form._meta.entangled_fields.items():
                    if field in fields:
                        if isinstance(value, models.Model):
                            # Correctly encode references
                            value = {
                                'model': f'{value._meta.app_label}.{value._meta.model_name}',
                                'pk': value.pk,
                            }
                        instance[container][field] = value
                        break
                else:
                    instance[field] = value
        else:
            instance.update(kwargs)
        # Create context
        context["instance"] = plugin_class.model(**instance)
        # Call render method of plugin
        context = plugin_class().render(context, context["instance"], None)
        # Replace inner plugins with the nodelist, i.e. the content within the plugin tag
        context["instance"].child_plugin_instances = DummyPlugin(
            nodelist, context["instance"].plugin_type
        ).get_instances()
        # ... and redner
        result = plugin_tag_pool[name]["template"].render(context.flatten())
        context.pop()
        return result


class RenderChildPluginsTag(Tag):
    """
    This template node is used to render child plugins of a plugin
    instance. It allows for selection of certain plugin types.

    e.g.: {% childplugins instance %}

    {% childplugins instance "LinkPlugin" %}

    {% placeholder "footer" inherit or %}
        <a href="/about/">About us</a>
    {% endplaceholder %}

    Keyword arguments:
    name -- the name of the placeholder
    inherit -- optional argument which if given will result in inheriting
        the content of the placeholder with the same name on parent pages
    or -- optional argument which if given will make the template tag a block
        tag whose content is shown if the placeholder is empty
    """

    name = "childplugins"
    options = Options(
        # PlaceholderOptions parses until the "endchildplugins" tag is found if
        # the "or" option is given
        Argument("instance", required=True),
        Argument("plugin_type", required=False),
        blocks=[("endchildplugins", "nodelist")],
    )

    def render_tag(self, context, instance, plugin_type, nodelist):
        context.push()
        context["parent"] = instance
        content = ""
        if plugin_type and not plugin_type.endswith("Plugin"):
            plugin_type = f"{instance.__class__.__name__}{plugin_type.capitalize()}Plugin"
        for child in instance.child_plugin_instances:
            if plugin_type is None or child.plugin_type == plugin_type:
                if isinstance(child, DummyPlugin):
                    content += child.nodelist.render(context)
                else:
                    content += render_plugin(context, child)
        content = content or getattr(instance, "simple_content", "")

        if not content.strip() and nodelist:
            # "or" parameter given
            return nodelist.render(context)

        context.pop()
        return content


class InlineField(CMSEditableObject):
    name = 'inline_field'
    options = Options(
        Argument('instance'),
        Argument('attribute'),
        Argument('language', default=None, required=False),
        Argument('filters', default=None, required=False),
        Argument('view_url', default=None, required=False),
        Argument('view_method', default=None, required=False),
        'as',
        Argument('varname', required=False, resolve=False),
    )

    def render_tag(self, context, **kwargs):
        if context["request"].session.get("inline_editing", True) and isinstance(kwargs["instance"], CMSPlugin):
            # Only allow inline field to be rendered if inline editing is active and the instance is a CMSPlugin
            # DummyPlugins of the ``plugin`` tag are cannot be edited
            kwargs["edit_fields"] = kwargs["attribute"]
            return super().render_tag(context, **kwargs)
        else:
            return getattr(kwargs["instance"], kwargs["attribute"], "")

    def _get_editable_context(self, context, instance, language, edit_fields,
                              view_method, view_url, querystring, editmode=True):
        # Fix a not-so-clean solution in django CMS' core: While the template engine checks if an attribute is
        # callable, python expects get_plugin_name to be a method. This is a workaround to make it a method.
        context = super()._get_editable_context(
            context, instance, language, edit_fields, view_method, view_url, querystring, editmode
        )
        if hasattr(instance, "get_plugin_name") and isinstance(instance.get_plugin_name, str):
            value = str(instance.get_plugin_name)
            instance.get_plugin_name = lambda: value
        return context


register.tag(Plugin.name, Plugin)
register.tag(RenderChildPluginsTag.name, RenderChildPluginsTag)
register.tag(InlineField.name, InlineField)
