from django import forms
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem

from .entry_model import FormEntry  # noqa


class Form(FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Form")


class FormFieldMixin:
    def get_short_description(self):
        label = self.config.get("field_label", "")
        return f"{label} ({self.config.get('field_name')})"


class CharField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Character field")

    def get_form_field(self):
        return self.field_name, forms.CharField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
            widget=forms.TextInput(
                attrs=dict(placeholder=self.config.get("field_placeholder", ""))
            ),
        )


class TextareaField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Text field")

    def get_form_field(self):
        return self.field_name, forms.CharField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
            widget=forms.Textarea(
                attrs=dict(
                    rows=self.config.get("field_rows", 10),
                    placeholder=self.config.get("field_placeholder", ""),
                    style="height: inherit;",
                )
            ),
        )


class Select(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Select")

    no_selection = [("", _("No selection"))]

    def get_form_field(self):
        multiple_choice = self.config.get("field_select", "") in (
            "mutliselect",
            "checkbox",
        )
        field = forms.MultipleChoiceField if multiple_choice else forms.ChoiceField
        required = self.config.get("field_required", False)
        choices = self.config.get("field_choices", ())
        if not required and not multiple_choice:
            choices = self.no_selection + choices
        widget_choice = self.config.get("field_select", "")
        if widget_choice == "select":
            widget = forms.Select()
        elif widget_choice == "radio":
            widget = forms.RadioSelect()
        elif widget_choice == "multiselect":
            widget = forms.SelectMultiple()
        else:
            widget = forms.CheckboxSelectMultiple()

        return self.field_name, field(
            label=self.config.get("field_label", ""),
            required=required,
            choices=choices,
            widget=widget,
        )


class MultiSelect(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Select multiple")


class SubmitButton(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Submit button")
