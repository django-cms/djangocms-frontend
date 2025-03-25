from django import forms, template

register = template.Library()


@register.simple_tag(takes_context=True)
def cms_component(context: template.Context, *args, **kwargs: dict) -> str:
    """
    Declare a CMS frontend component in a Django template.

    This template tag triggers the generation of a CMS frontend component
    class based on the implate it is part of. The component class is generated
    with the provided arguments as ``Meta`` properties.

    Args:
        context (template.Context): The Django template context object where
            components are stored.
        name: Internal name of the component. Must be unique throught a project.
        **kwargs: Keyword arguments to be added to component's ``Meta`` class list.

    Returns:
        str: An empty string, as this function is intended for side effects only.
    """
    if "_cms_components" in context:
        if len(args) != 1:  # pragma: no cover
            raise ValueError("The cms_component tag requires exactly one positional argument: the component name.")
        context["_cms_components"]["cms_component"].append((args, kwargs))
    return ""


@register.simple_tag(takes_context=True)
def field(context: template.Context, field_name: str, field_type: forms.Field, **kwargs) -> str:
    """
    Declares a field entry for the component. It only has an effect if used in
    conjunction with ``{% cms_component %}``.

    Args:
        context (template.Context): The template context object that may contain
            the "_cms_components" dictionary.
        field_name (str): The name of the field to be added to the component.
        field_type (forms.Field): A Django form field class to be used for the field.
        **kwargs: Arbitrary keyword arguments representing field attributes or data.

    Returns:
        str: An empty string, as this function is intended for side effects only.
    """
    if "_cms_components" in context:
        context["_cms_components"]["fields"].append(([field_name, field_type], kwargs))
    return ""


@register.filter
def split(value: str, delimiter: str = "|") -> list[str]:
    """
    Helper that splits a given string into a list of substrings based on a specified delimiter.

    Args:
        value (str): The string to be split.
        delimiter (str, optional): The delimiter to use for splitting the string. Defaults to "|".

    Returns:
        list[str]: A list of substrings obtained by splitting the input string using the delimiter.
    """
    return value.split(delimiter)
