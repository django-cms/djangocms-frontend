import decimal

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


class EmailField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Email field")

    def get_form_field(self):
        return self.field_name, forms.EmailField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
        )


class UrlField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("URL field")

    def get_form_field(self):
        return self.field_name, forms.URLField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
        )


class DecimalField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Decimal field")

    class NumberInput(forms.NumberInput):
        def __init__(self, **kwargs):
            self.decimal_places = kwargs.pop("decimal_places", None)
            super().__init__(**kwargs)

        def format_value(self, value):
            value = str(value)
            l, r = value.rsplit(".", 1)
            if self.decimal_places == 0:
                return l
            r = (r + self.decimal_places * "0")[: self.decimal_places]
            return super().format_value(".".join((l, r)))

    class StrDecimalField(forms.DecimalField):
        def clean(self, value):
            value = super().clean(value)
            if isinstance(value, decimal.Decimal):
                value = str(value)
            return value

    def get_form_field(self):
        return self.field_name, DecimalField.StrDecimalField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
            min_value=self.config.get("min_value", None),
            max_value=self.config.get("max_value", None),
            decimal_places=self.config.get("decimal_places", None),
            widget=DecimalField.NumberInput(
                decimal_places=self.config.get("decimal_places", None)
            ),
        )


class IntegerField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Integer field")

    def get_form_field(self):
        return self.field_name, forms.IntegerField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
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

    _choices = None
    no_selection = [("", _("No selection"))]

    def get_choices(self):
        if self._choices is None:
            descendants = self.get_children().order_by("position")
            self._choices = []
            for child in descendants:
                instance = child.djangocms_frontend_frontenduiitem
                self._choices.append(
                    (instance.config["value"], instance.config["verbose"])
                )
        return self._choices

    def get_form_field(self):
        multiple_choice = self.config.get("field_select", "") in (
            "multiselect",
            "checkbox",
        )
        field = forms.MultipleChoiceField if multiple_choice else forms.ChoiceField
        required = self.config.get("field_required", False)
        choices = self.get_choices()
        if not required and not multiple_choice:
            choices = self.no_selection + choices
        widget_choice = self.config.get("field_select", "")
        if widget_choice == "select":
            widget = forms.Select()
        elif widget_choice == "radio":
            widget = forms.RadioSelect()
        elif widget_choice == "multiselect":
            widget = forms.SelectMultiple(attrs=dict(style="min-height: 6em;"))
        else:
            widget = forms.CheckboxSelectMultiple()

        return self.field_name, field(
            label=self.config.get("field_label", ""),
            required=required,
            choices=choices,
            widget=widget,
        )


class Choice(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Choice")

    def get_short_description(self):
        return f'{self.config.get("verbose", "-")} ("{self.config.get("value", "")}")'


class SwitchInput(forms.CheckboxInput):
    pass


class BooleanField(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Boolean field")

    def get_form_field(self):
        return self.field_name, forms.BooleanField(
            label=self.config.get("field_label", ""),
            required=self.config.get("field_required", False),
            widget=SwitchInput()
            if self.config.get("field_as_switch", False)
            else forms.CheckboxInput(),
        )


class SubmitButton(FormFieldMixin, FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Submit button")
