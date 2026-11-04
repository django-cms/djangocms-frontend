"""Translate configuration values for framework-specific templates."""

from django import template

from djangocms_frontend.models import is_plugin_type

register = template.Library()


@register.filter
def framework_value(instance, field):
    resolver = getattr(instance, "get_framework_value", None)
    return resolver(field) if resolver is not None else ""


@register.simple_tag
def parent_framework_value(instance, plugin_type, field):
    """Resolve a parent option without depending on a particular render mixin."""
    resolver = getattr(instance, "get_parent_framework_value", None)
    return resolver(plugin_type, field) if resolver is not None else ""


@register.filter(name="is_plugin_type")
def is_plugin_type_filter(plugin_type, base):
    """``{% if plugin.plugin_type|is_plugin_type:"CardPlugin" %}`` also matches subclasses."""
    return bool(plugin_type) and is_plugin_type(plugin_type, base)
