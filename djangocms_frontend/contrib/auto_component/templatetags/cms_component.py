from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def cms_component(context, *args, **kwargs):
    if "_cms_components" in context:
        context["_cms_components"]["cms_component"].append((args, kwargs))
    return ""


@register.simple_tag(takes_context=True)
def field(context, *args, **kwargs):
    if "_cms_components" in context:
        context["_cms_components"]["fields"].append((args, kwargs))
    return ""
