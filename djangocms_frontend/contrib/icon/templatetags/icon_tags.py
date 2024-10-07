from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from djangocms_frontend.contrib.icon.conf import ICON_LIBRARIES

register = template.Library()


@register.inclusion_tag("djangocms_frontend/icon/add_css.html", takes_context=True)
def add_css_for_icon(context, icon):
    if icon and icon.get("library", "") in ICON_LIBRARIES:
        css_link = ICON_LIBRARIES[icon.get("library")][1]
        if css_link:
            if "/" not in css_link:  # static link?
                css_link = static(f"djangocms_frontend/icon/vendor/assets/stylesheets/{css_link}")
            context["icon_css"] = css_link
    return context


@register.simple_tag(takes_context=True)
def icon(context, icon):
    if icon:
        icon_class = icon.get("iconClass", "")
        icon_text = icon.get("iconText", "")
        return mark_safe(f'<i class="{icon_class}">{icon_text}</i>')
    return ""
