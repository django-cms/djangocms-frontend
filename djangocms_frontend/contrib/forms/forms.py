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
    ButtonGroup,
    ChoicesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem

from . import constants

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
    takes_request = True

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop("request")
        if get_option(self, "unique", False) and self._request.user.is_authenticated:
            qs = FormEntry.objects.filter(
                form_user=self._request.user, form_name=get_option(self, "form_name")
            )
            if qs:
                kwargs["initial"] = qs.last().entry_data
        super().__init__(*args, **kwargs)

    def clean(self):
        if get_option(self, "login_required", False):
            if not self._request.user.is_authenticated:
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
                "entry_data": self.cleaned_data,
                "html_headers": dict(
                    user_agent=self._request.headers["User-Agent"],
                    referer=self._request.headers["Referer"],
                ),
            }
        )
        if keys:  # update_or_create only works if at least one key is given
            try:
                FormEntry.objects.update_or_create(**keys, defaults=defaults)
            except FormEntry.MultipleObjectsReturned:  # Delete outdated objects
                FormEntry.objects.filter(**keys).delete()
                FormEntry.objects.create(**keys, **defaults)
        else:
            FormEntry.objects.create(**defaults), True
        if get_option(self, "email", []):
            raise NotImplementedError("email notification for forms")


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
                "form_login_required",
                "form_unique",
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
    )
    form_name = forms.CharField(
        label=_("Form name"),
        required=False,
        initial="",
        validators=[
            validate_slug,
        ],
    )
    form_login_required = forms.BooleanField(
        label=_("Login required to submit form"),
        required=False,
        initial=False,
        help_text=_(
            "To avoid issues with user experience use this type of form only on pages, "
            "which require login."
        ),
    )

    form_unique = forms.BooleanField(
        label=_("User can reopen form"),
        required=False,
        initial=False,
        help_text=_('Requires "Login required" to be checked to work.'),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registered_forms = get_registered_forms()
        self.fields["form_selection"].widget = (
            forms.Select() if _form_registry else forms.HiddenInput()
        )
        self.fields["form_selection"].choices = registered_forms

    def clean(self):
        if self.cleaned_data["form_selection"] == "":
            if not self.cleaned_data["form_name"]:
                raise ValidationError(
                    {
                        "form_name": _(
                            "Please provide a form name to be able to evaluate form submissions."
                        )
                    },
                    code="incomplete",
                )
        if (
            self.cleaned_data["form_unique"]
            and not self.cleaned_data["form_login_required"]
        ):
            error = _("Users can only reopen forms if they are logged in. %(remedy)s")
            raise ValidationError(
                {
                    "form_login_required": error
                    % dict(remedy=_("Either enable this.")),
                    "form_unique": _("Or disable this."),
                },
                code="inconsistent",
            )


FORBIDDEN_FORM_NAMES = [
    "Meta",
    "get_success_context",
    "form_name",
    "form_user",
    "entry_data",
    "html_header",
] + dir(SimpleFrontendForm(request=None))


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
                "min_length",
                "max_length",
            ]
        }

    min_length = forms.IntegerField(
        label=_("Minimum text length"),
        required=False,
        initial=None,
    )
    max_length = forms.IntegerField(
        label=_("Minimum text length"),
        required=False,
        initial=None,
    )


class EmailFieldForm(mixin_factory("EmailField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}


class UrlFieldForm(mixin_factory("URLField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}


class DecimalFieldForm(
    mixin_factory("DecimalField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "min_value",
                "max_value",
                "decimal_places",
            ]
        }

    min_value = forms.DecimalField(
        label=_("Minimum value"),
        required=False,
        initial=None,
    )
    max_value = forms.DecimalField(
        label=_("Maximum value"), required=False, initial=None
    )
    decimal_places = forms.IntegerField(
        label=_("Decimal places"),
        required=False,
        initial=None,
        min_value=0,
    )


class IntegerFieldForm(
    mixin_factory("IntegerField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "min_value",
                "max_value",
            ]
        }

    min_value = forms.IntegerField(
        label=_("Minimum value"),
        required=False,
        initial=None,
    )
    max_value = forms.IntegerField(
        label=_("Maximum value"), required=False, initial=None
    )


class TextareaFieldForm(
    mixin_factory("TextareaField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "min_length",
                "max_length",
                "field_rows",
            ]
        }

    field_rows = forms.IntegerField(
        label=_("Rows"),
        min_value=1,
        max_value=40,
        initial=10,
        help_text=_("Defines the vertical size of the text area in number of rows."),
    )
    min_length = forms.IntegerField(
        label=_("Minimum text length"),
        required=False,
        initial=None,
    )
    max_length = forms.IntegerField(
        label=_("Minimum text length"),
        required=False,
        initial=None,
    )


class DateFieldForm(mixin_factory("DateField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}


class DateTimeFieldForm(
    mixin_factory("DateTimeField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}


class TimeFieldForm(mixin_factory("TimeField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}


class SelectFieldForm(mixin_factory("SelectField"), FormFieldMixin, EntangledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" in kwargs and kwargs["instance"] is not None:
            self.fields["field_choices"].initial = kwargs["instance"].get_choices()

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "field_select",
            ]
        }
        untangled_fields = ("field_choices",)

    field_select = forms.ChoiceField(
        label=_("Selection type"),
        required=True,
        choices=constants.CHOICE_FIELDS,
        widget=ButtonGroup(
            attrs=dict(property="text", label_class="btn-outline-secondary")
        ),
    )
    field_choices = ChoicesFormField(
        required=True,
        help_text=_(
            "Use this field to quick edit choices. Choices can be added (<kbd>+</kbd>), deleted (<kbd>&times;</kbd>) "
            "and updated. On the left side enter the value to be stored in the database. On the right side enter the "
            "text to be shown to the user. The order of choices can be adjusted in the structure tree after saving "
            "the edits."
        ),
    )


class ChoiceForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "value",
                "verbose",
            ]
        }

    value = forms.CharField(
        label=_("Value"),
        required=True,
        help_text=_("Stored in database if the choice is selected."),
    )
    verbose = forms.CharField(
        label=_("Display text"),
        required=True,
        help_text=_("Representation of choice displayed to the user."),
    )


class BooleanFieldForm(
    mixin_factory("BooleanField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "field_as_switch",
            ]
        }

    field_as_switch = forms.BooleanField(
        label=_("As switch"),
        initial=False,
        required=False,
        help_text=_("If set the boolean field will offer a switch widget."),
    )
