import hashlib

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm, EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.contrib import forms as forms_module
from djangocms_frontend.contrib.forms.entry_model import FormEntry
from djangocms_frontend.contrib.forms.helper import get_option
from djangocms_frontend.fields import (
    AttributesFormField,
    ChoicesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem, models

mixin_factory = settings.get_forms(forms_module)


_form_registry = {}


def verbose_name(form_class):
    """returns the verbose_name property of a Meta class if present or else
    splits the camel-cased form class name"""
    if hasattr(form_class, "Meta") and hasattr(form_class.Meta, "verbose_name"):
        return getattr(form_class.Meta, "verbose_name")  # noqa
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


class SimpleFrontendForm(forms.Form):
    # def __init__(self, data=None, *args, **kwargs):
    #     if data is None:
    #         if hasattr(self, "_request") and get_option(self, "unqiue", False):
    #             ...
    #
    #     super().__init__(self, data=data, *args, **kwargs)
    #
    def clean(self):
        if get_option(self, "login_required", False):
            if not hasattr(self, "_request") or not self._request.user.is_authenticated:
                raise ValidationError(
                    _("Please login before submitting this form."), code="unauthorized"
                )
        super().clean()

    def save(self):
        if get_option(self, "unique", False) and get_option(
            self, "login_required", False
        ):
            keys = {
                "form_name": get_option(self, "form_name"),
                "form_user": self._request.user,
            }
            defaults = {}
        else:
            keys = {}
            defaults = {
                "form_name": get_option(self, "form_name"),
                "form_user": self._request.user,
            }
        defaults.update(
            {
                "entry_data": {
                    key: self.serialize(value)
                    for key, value in self.cleaned_data.items()
                },
                "html_headers": dict(
                    user_agent=self._request.headers["User-Agent"],
                    referer=self._request.headers["Referer"],
                ),
            }
        )
        if keys:  # update_or_create only works if at least one key is given
            obj, created = FormEntry.objects.update_or_create(
                **keys, defaults=defaults
            )  # noqa
        else:
            obj, created = FormEntry.objects.create(**defaults), True  # noqa
        if get_option(self, "email", []):
            raise NotImplementedError("email notification for forms")

    def serialize(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, models.Model):
            return "Not implemented"
        if isinstance(value, (list, tuple)):
            return ", ".join(map(self.serialize, value))
        if hasattr(value, "__str__"):
            return str(value)
        return "Cannot save"


class FormsForm(mixin_factory("Form"), EntangledModelForm):
    """
    Components > "Forms" Plugin
    https://getbootstrap.com/docs/5.1/forms/overview/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "form_selection",
                "form_name",
                "form_floating_labels",
                "form_spacing",
                "form_submit_message",
                "form_submit_context",
                "form_submit_align",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    form_selection = forms.ChoiceField(
        label=_("Form"),
        required=False,
        initial="",
        choices=get_registered_forms,
    )
    form_name = forms.CharField(
        label=_("Form name"),
        required=False,
        initial="",
        validators=[
            validate_slug,
        ],
    )
    form_floating_labels = forms.BooleanField(
        label=_("Floating labels"),
        required=False,
        initial=False,
    )
    form_spacing = forms.ChoiceField(
        label=_("Margin between fields"),
        choices=settings.SPACER_SIZE_CHOICES,
        initial=settings.SPACER_SIZE_CHOICES[len(settings.SPACER_SIZE_CHOICES) // 2][0],
    )
    form_submit_message = forms.CharField(
        label=_("Submit message"),
        initial=_("Submit"),
        required=True,
    )
    form_submit_context = forms.ChoiceField(
        label=_("Submit context"),
        choices=settings.COLOR_STYLE_CHOICES,
        initial=first_choice(settings.COLOR_STYLE_CHOICES),
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
    tag_type = TagTypeFormField()


FORBIDDEN_FORM_NAMES = [
    "Meta",
    "get_success_context",
    "form_name",
    "form_user",
    "entry_data",
    "html_header",
] + dir(SimpleFrontendForm())


def validate_form_name(value):
    if value in FORBIDDEN_FORM_NAMES:
        raise ValidationError(
            _("This name is reserved. Please chose a different one."), code="illegal"
        )


class FormFieldMixin(EntangledModelFormMixin):
    """
    Components > "Forms" Plugin
    https://getbootstrap.com/docs/5.1/forms/overview/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "field_name",
                "field_label",
                "field_placeholder",
                "field_required",
            ]
        }

    field_name = forms.CharField(
        label=_("Field name"),
        required=True,
        validators=[validate_slug, validate_form_name],
    )
    field_label = forms.CharField(
        label=_("Label"),
        required=False,
    )
    field_placeholder = forms.CharField(
        label=_("Placeholder"),
        required=False,
    )
    field_required = forms.BooleanField(
        label=_("Required"),
        initial=False,
        required=False,
    )


class CharFieldForm(mixin_factory("CharField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "attributes",
            ]
        }

    attributes = AttributesFormField()


class TextareaFieldForm(
    mixin_factory("TextareaField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "field_rows",
                "attributes",
            ]
        }

    field_rows = forms.IntegerField(
        label=_("Rows"),
        min_value=1,
        max_value=40,
        initial=10,
        help_text=_("Defines the vertical size of the text area in number of rows."),
    )
    attributes = AttributesFormField()


class SelectFieldForm(mixin_factory("SelectField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "field_choices",
                "field_select",
                "attributes",
            ]
        }

    field_select = forms.ChoiceField(
        label=_("Selection type"),
        required=True,
        choices=(
            ("select", _("Drop down (single choice)")),
            ("multiselect", _("List (multiple choice)")),
            ("radio", _("Radio buttons (single choice)")),
            ("checkbox", _("Checkboxes (multiple choice")),
        ),
    )
    field_choices = ChoicesFormField(
        required=True,
        help_text=_(
            "Please provide the choices. Add with <code>+</code>. In the left field enter the "
            "value to be stored. In the right field enter the text to be shown to the user."
        ),
    )
    attributes = AttributesFormField()
