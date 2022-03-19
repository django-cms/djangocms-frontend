import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.html import conditional_escape, mark_safe

from djangocms_frontend import settings
from djangocms_frontend.helpers import get_related_object as related_object

register = template.Library()


@register.simple_tag
def get_attributes(attribute_field, *add_classes):
    """Joins a list of classes with an attributes field and returns all html attributes"""
    additional_classes = set()
    for classes in add_classes:
        if classes:
            additional_classes.update(
                classes.split() if isinstance(classes, str) else classes
            )
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
            model_name = (
                ContentType.objects.get(id=content_type_id).model_class().__name__
            )
            framework_info = settings.FRAMEWORK_PLUGIN_INFO.get(model_name, {})
            context["framework_info"] = framework_info  # and store
    return (
        mark_safe(json.dumps(framework_info.get(item, ""), cls=LazyEncoder))
        if as_json
        else framework_info.get(item, "")
    )
