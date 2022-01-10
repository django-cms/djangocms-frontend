from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def classes_and_attributes(context, additional_classes=""):
    """Joins a list of classes with the attributes field and returns all attributes"""
    instance = context["instance"]
    classes = set(additional_classes.split() + instance.attributes.get("class").split())
    instance.attributes["class"] = " ".join(classes)
    return instance.attributes_str
