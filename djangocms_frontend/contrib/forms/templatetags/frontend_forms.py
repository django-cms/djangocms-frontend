from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import mark_safe

from djangocms_frontend.contrib.forms import constants
from djangocms_frontend.settings import FORM_TEMPLATE

register = template.Library()
attr_dict = constants.attr_dict
default_attr = constants.default_attr


try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.utils import render_crispy_form as render_form_implementation

    crispy_forms_installed = True
except ImportError:
    crispy_forms_installed = False

    def render_form_implementation(form, helper=None, context=None):
        return str(form)

    class FormHelper:
        def __init__(self, form):
            self.form = form


global_options = getattr(settings, "DJANGOCMS_FRONTEND_FORM_OPTIONS", {})


def get_option(form, option, default=None):
    form_options = getattr(getattr(form, "Meta", None), "options", {})
    return form_options.get(option, global_options.get(option, default))


@register.filter
def add_placeholder(form):
    """Adds placeholder based on a form field's title"""
    for field_name, field in form.fields.items():
        form.fields[field_name].widget.attrs["placeholder"] = form.fields[
            field_name
        ].label
    return form


@register.simple_tag()
def render_form(form, **kwargs):
    """Renders form either with crispy_forms if installed and form has helper or with
    djangocms-frontend's means"""
    if crispy_forms_installed:
        helper = kwargs.pop("helper", None) or getattr(form, "helper", None)
        if helper is None and get_option(form, "crispy_form"):
            helper = FormHelper(form=form)
        if helper is not None:
            helper.form_tag = False
            helper.disable_csrf = True
            return mark_safe(render_form_implementation(form, helper, None))
    template = kwargs.pop("template", FORM_TEMPLATE)
    return render_to_string(template, {"form": form, **kwargs})


def get_bound_field(form, formfield):
    for field in form.visible_fields():
        if field.name == formfield:
            return field
    return None


def attrs_for_widget(widget, item, additional_classes=None):
    if widget.__class__.__name__ in constants.attr_dict:
        cls = attr_dict[widget.__class__.__name__].get(item, None)
    else:
        cls = default_attr[item]
    if cls:
        if additional_classes:
            cls += " " + additional_classes
    else:
        cls = additional_classes or ""
    return {"class": cls}


@register.simple_tag(takes_context=True)
def render_widget(context, form, form_field, **kwargs):
    field = get_bound_field(form, form_field)
    if field is None:
        return ""
    floating_labels = get_option(form, "floating_labels")
    field_sep = get_option(form, "field_sep", constants.DEFAULT_FIELD_SEP)
    widget_attr = kwargs
    if form.is_bound:
        add_classes = "is_invalid" if field.errors else "is_valid"
    else:
        add_classes = None
    widget_attr.update(
        attrs_for_widget(field.field.widget, "input", additional_classes=add_classes)
    )
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
    errors = "".join(
        f'<div class="invalid-feedback">{error}</div>' for error in field.errors
    )
    if floating_labels or input_type == "checkbox" or input_type == "select":
        render = f"<div {div_attrs}>{widget}{label}{errors}{help_text}</div>"
    else:
        render = f"<div {div_attrs}>{label}{widget}{errors}{help_text}</div>"
    return mark_safe(render)


@register.filter_function
def get_fieldset(form):
    """returns the fieldsets of a form if available or generates a fieldset as a
    list of all fields"""
    if hasattr(form, "get_fieldsets") and callable(form.get_fieldsets):
        return form.get_fieldsets()
    elif hasattr(form, "Meta") and hasattr(form.Meta, "fieldsets"):
        return form.Meta.fieldsets
    return ((None, {"fields": [field.name for field in form.visible_fields()]}),)
