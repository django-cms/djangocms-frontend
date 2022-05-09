from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm, EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.contrib import frontend_forms
from djangocms_frontend.contrib.frontend_forms.entry_model import FormEntry
from djangocms_frontend.contrib.frontend_forms.helper import get_option
from djangocms_frontend.fields import (
    AttributesFormField,
    ButtonGroup,
    ChoicesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice, mark_safe_lazy
from djangocms_frontend.models import FrontendUIItem

from . import _form_registry, actions, constants, get_registered_forms, recaptcha

mixin_factory = settings.get_forms(frontend_forms)


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
        return super().clean()

    def save(self):
        results = {}
        form_actions = get_option(self, "form_actions", [])
        for action in form_actions:
            Action = actions.get_action_class(action)
            if Action is not None:
                results[action] = Action().execute(self, self._request)
            else:
                results[action] = _("Action not available any more")
        if not form_actions:
            results[None] = _("No action registered")


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
                "form_actions",
                "attributes",
                "captcha_widget",
                "captcha_requirement",
                "captcha_config",
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

    _available_form_actions = actions.get_registered_actions()
    form_actions = forms.MultipleChoiceField(
        label=_("Actions to be taken after form submission"),
        choices=_available_form_actions,
        initial=first_choice(_available_form_actions),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
    )

    attributes = AttributesFormField()

    captcha_widget = forms.ChoiceField(
        label=_("reCaptcha widget"),
        required=False,
        initial="v2-invisible" if recaptcha.installed else "",
        choices=settings.EMPTY_CHOICE + recaptcha.RECAPTCHA_CHOICES,
        help_text=mark_safe_lazy(
            _(
                'Read more in the <a href="{link}" target="_blank">documentation</a>.'
            ).format(link="https://developers.google.com/recaptcha")
        ),
    )
    captcha_requirement = forms.DecimalField(
        label=_("Minimum score requirement"),
        required=recaptcha.installed,
        initial=0.5,
        min_value=0,
        max_value=1,
        help_text=_(
            "Only for reCaptcha v3: Minimum score required to accept challenge."
        ),
    )
    captcha_config = AttributesFormField(
        label=_("Recaptcha configuration parameters"),
        help_text=mark_safe_lazy(
            _(
                'The reCAPTCHA widget supports several <a href="{attr_link}" target="_blank">data attributes</a> '
                "that customize the behaviour of the widget, such as <code>data-theme</code>, "
                "<code>data-size</code>. "
                'The reCAPTCHA api supports several <a href="{api_link}" target="_blank">parameters</a>. '
                "Add these api parameters as attributes, e.g. <code>hl</code> to set the language."
            ).format(
                attr_link="https://developers.google.com/recaptcha/docs/display#render_param",
                api_link="https://developers.google.com/recaptcha/docs/display#javascript_resource_apijs_parameters",
            )
        ),
    )
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

        if "form_actions" in self.cleaned_data:
            if (
                self.cleaned_data["form_unique"]
                and actions.SAVE_TO_DB_ACTION not in self.cleaned_data["form_actions"]
            ):
                if actions.SAVE_TO_DB_ACTION:
                    raise ValidationError(
                        {
                            "form_actions": _(
                                'Please select "Save form submission" to allow users to reopen forms.'
                            ),
                            "form_unique": _(
                                'Please select the action "Save form submission" to allow users to reopen forms.'
                            ),
                        }
                    )
                else:
                    raise ValidationError(
                        {
                            "form_unique": _(
                                "No form action to save form contents available. Users will not be "
                                "able to reopen a form."
                            ),
                        }
                    )
        else:
            raise ValidationError(
                {
                    "form_actions": _(
                        "At least one action needs to be selected for the form to have an effect."
                    ),
                }
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
        return self.cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        print("XXX", self.errors, self.non_field_errors())
        return valid


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
        label=_("Maximum text length"),
        required=False,
        initial=None,
    )


class DateFieldForm(mixin_factory("DateField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["field_placeholder"].help_text = _("Not visible on most browsers.")


class DateTimeFieldForm(
    mixin_factory("DateTimeField"), FormFieldMixin, EntangledModelForm
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["field_placeholder"].help_text = _("Not visible on most browsers.")


class TimeFieldForm(mixin_factory("TimeField"), FormFieldMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["field_placeholder"].help_text = _("Not visible on most browsers.")


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
    )

    def clean(self):
        if (
            self.cleaned_data.get("field_required", False)
            and self.cleaned_data.get("field_select", "") == "checkbox"
        ):
            raise ValidationError(
                {
                    "field_select": mark_safe_lazy(
                        _(
                            "For a required multiple choice fild select the <b>list</b> selection type."
                        )
                    ),
                    "field_required": mark_safe_lazy(
                        _("Checkbox multiple choice field <b>must not be required</b>.")
                    ),
                }
            )
        return self.cleaned_data


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
        label=_("Layout"),
        initial=False,
        required=False,
        widget=ButtonGroup(
            choices=((False, _("Checkbox")), (True, _("Switch"))),
            attrs=dict(property="text", label_class="btn-outline-secondary"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["field_required"].help_text = _(
            "If checked, the form can only be submitted if the "
            "checkbox is checked or the switch set to on."
        )
