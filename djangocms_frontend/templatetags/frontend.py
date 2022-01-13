from django import template
from django.utils.html import conditional_escape, mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def classes_and_attributes(
    context, additional_classes="", attribute_field="attributes", excluded_keys=""
):
    """Joins a list of classes with the attributes field of the instance given in context
    and returns all attributes"""
    attributes = getattr(context["instance"], attribute_field)
    attrs = []
    for key, val in attributes.items():
        if key.lower() not in excluded_keys:
            if key.lower() == "class":
                val += " " + additional_classes
            if val:
                attrs.append(
                    '{key}="{value}"'.format(key=key, value=conditional_escape(val))
                )
            else:
                attrs.append("{key}".format(key=key))
    return mark_safe(" ".join(attrs))
