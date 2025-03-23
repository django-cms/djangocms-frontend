from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def cms_component(context: template.Context, *args, **kwargs) -> str:
    if "_cms_components" in context:
        context["_cms_components"]["cms_component"].append((args, kwargs))
    return ""


@register.simple_tag(takes_context=True)
def field(context: template.Context, *args, **kwargs) -> str:
    if "_cms_components" in context:
        context["_cms_components"]["fields"].append((args, kwargs))
    return ""


@register.filter
def split(value: str, delimiter: str = "|") -> list[str]:
    return value.split(delimiter)
