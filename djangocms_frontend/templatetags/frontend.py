from django import template
from django.utils.html import conditional_escape, mark_safe
from entangled.utils import get_related_object as related_object

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
                attrs.append(
                    '{key}="{value}"'.format(key=key, value=conditional_escape(val))
                )
            else:
                attrs.append("{key}".format(key=key))
    if additional_classes and (not attribute_field or "class" not in attribute_field):
        attrs.append(f'class="{conditional_escape(" ".join(additional_classes))}"')
    return mark_safe(" ".join(attrs))


@register.filter
def get_related_object(reference):
    return related_object(dict(obj=reference), "obj")
