from django import template
from django.utils.html import mark_safe

register = template.Library()

try:
    from crispy_forms.utils import render_crispy_form as render_form_implementation

except ImportError:

    def render_form_implementation(form, helper=None, context=None):
        return str(form)


@register.simple_tag(takes_context=True)
def render_form(context, form, helper=None):
    """Joins a list of classes with an attributes field and returns all html attributes"""
    return mark_safe(render_form_implementation(form, helper, None))
