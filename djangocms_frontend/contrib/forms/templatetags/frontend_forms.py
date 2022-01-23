import functools

from django import template
from django.utils.html import mark_safe

register = template.Library()

try:
    from crispy_forms.utils import render_crispy_form as render_form_implementation
    from crispy_forms.helper import FormHelper
except ImportError:

    def render_form_implementation(form, helper=None, context=None):
        return str(form)

    class FormHelper:
        def __init__(self, form):
            self.form = form


@register.simple_tag(takes_context=True)
def render_form(context, form, helper=None):
    """Joins a list of classes with an attributes field and returns all html attributes"""
    if helper is None:
        helper = getattr(form, "helper", None)
    if helper is None:
        helper = FormHelper(form)
    helper.form_tag = False
    helper.disable_csrf = True
    return mark_safe(render_form_implementation(form, helper, None))


default_attr = dict(
    input="form-control",
    label="form-label",
    div="",
)

attr_dict = dict(
    Select=dict(input="form-select"),
    SelectMultiple=dict(input="form-select"),
    NullBooleanSelect=dict(input="form-select"),
    RadioSelect=dict(
        input="form-check-input", label="form-check-label", div="form-check"
    ),
    CheckboxInput=dict(
        input="form-check-input", label="form-check-label", div="form-check"
    ),
    ButtonRadio=dict(input="btn-check", label="btn btn-outline-primary"),
    ButtonCheckbox=dict(input="btn-check", label="btn btn-outline-primary"),
)


def get_bound_field(form, formfield):
    for field in form.visible_fields():
        if field.name == formfield:
            return field
    return None


def attrs_for_widget(widget, item, additional_classes=None):
    if widget.__class__.__name__ in attr_dict:
        cls = attr_dict[widget.__class__.__name__].get(item, None)
    else:
        cls = default_attr[item]
    if cls:
        if additional_classes:
            cls += " " + additional_classes
    else:
        cls = (additional_classes or "")
    return {"class": cls}


@register.simple_tag(takes_context=True)
def render_widget(context, form, form_field, **kwargs):
    field = get_bound_field(form, form_field)
    if field is None:
        return ""
    options = getattr(form, "frontend_options", {})
    floating_labels = "floating_labels" in options
    field_sep = options.get("field_sep", "mb-3")
    widget_attr = kwargs
    widget_attr.update(attrs_for_widget(field.field.widget, "input"))
    label_attr = attrs_for_widget(field.field.widget, "label")
    if field.help_text:
        widget_attr.update({"aria-describedby": f"hints_{field.id_for_label}"})
        help_text = f'<div id="hints_{field.id_for_label}" class="form-text">{field.help_text}</div>'
    else:
        help_text = ""
    if floating_labels:
        widget_attr.setdefault("placeholder", "-")
        field_sep += " form-floating"
    div_attrs = attrs_for_widget(field.field.widget, "div", field_sep)
    div_attrs = " ".join([f'{key}="{value}"' for key, value in div_attrs.items()])
    label = field.label_tag(attrs=label_attr)
    widget = field.as_widget(attrs=widget_attr)
    input_type = getattr(field.field.widget, "input_type", None)
    if floating_labels or input_type == "checkbox" or input_type == "select":
        render = f'<div {div_attrs}>{widget}{label}{help_text}</div>'
    else:
        render = f'<div {div_attrs}>{label}{widget}{help_text}</div>'
    return mark_safe(render)



@register.filter_function
def get_fieldset(form):
    """returns the fieldsets of a form if available or generates a fieldset as a
    list of all fields"""
    if hasattr(form, "fieldsets"):
        return form.fieldsets
    elif hasattr(form, "get_fieldsets") and callable(form.get_fieldsets):
        return form.get_fieldsets()
    return ((None, {"fields": [field.name for field in form.visible_fields()]}),)

