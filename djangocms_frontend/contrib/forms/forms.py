import hashlib

from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.contrib import forms as forms_module
from djangocms_frontend.fields import AttributesFormField, ColoredButtonGroup
from djangocms_frontend.models import FrontendUIItem

mixin_factory = settings.get_forms(forms_module)


_form_registry = {}


def verbose_name(form_class):
    """returns the verbose_name property of a Meta class if present or else
    splits the camel-cased form class name"""
    if hasattr(form_class, "Meta") and hasattr(form_class.Meta, "verbose_name"):
        return getattr(form_class.Meta, "verbose_name")
    class_name = form_class.__name__.rsplit(".", 1)[-1]
    from re import finditer

    matches = finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", class_name
    )
    return " ".join(m.group(0) for m in matches)


def get_registered_forms():
    """Creates a tuple for a ChoiceField to select form"""
    result = tuple(
        (hash, verbose_name(form_class)) for hash, form_class in _form_registry.items()
    )
    return result if result else ((_("No forms registered"), ()),)


def register(form_class):
    """Function to call or decorator for a Form class to make it available for the
    djangocms_frontend.contrib.forms plugin"""
    hash = hashlib.sha1(form_class.__name__.encode("utf-8")).hexdigest()
    _form_registry.update({hash: form_class})
    return form_class


class FormsForm(mixin_factory("Form"), EntangledModelForm):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "form_selection",
                "form_submit_message",
                "form_submit_context",
                "form_submit_align",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    form_selection = forms.ChoiceField(
        label=_("Form"),
        required=True,
        initial="",
        choices=get_registered_forms,
    )

    form_submit_message = forms.CharField(
        label=_("Submit message"),
        initial=_("Submit"),
        required=True,
    )
    form_submit_context = forms.ChoiceField(
        label=_("Submit context"),
        choices=settings.COLOR_STYLE_CHOICES,
        initial=settings.COLOR_STYLE_CHOICES[0][0],
        required=True,
        widget=ColoredButtonGroup(),
    )
    form_submit_align = forms.ChoiceField(
        label=_("Submit button alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
    )
    attributes = AttributesFormField()
