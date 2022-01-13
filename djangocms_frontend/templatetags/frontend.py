from django import template
from django.utils.html import conditional_escape, mark_safe

register = template.Library()


@register.simple_tag
def add_class(attribute_field, *add_classes):
    """Joins a list of classes with an attributes field and returns all html attributes"""
    additional_classes = " ".join(add_classes)
    attrs = []
    for key, val in attribute_field.items():
        if key.lower() == "class":
            val += " " + additional_classes
        if val:
            attrs.append(
                '{key}="{value}"'.format(key=key, value=conditional_escape(val))
            )
        else:
            attrs.append("{key}".format(key=key))
    if additional_classes and "class" not in attribute_field:
        attrs.append(f'class="{conditional_escape(additional_classes)}"')
    return mark_safe(" ".join(attrs))
