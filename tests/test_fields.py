from django import forms
from django.test import TestCase

from djangocms_frontend.fields import (
    AttributesField,
    DeviceChoiceField,
    OptionalDeviceChoiceField,
    TagTypeField,
    TagTypeFormField,
)
from djangocms_frontend.settings import DEVICE_CHOICES


class FieldsTestCase(TestCase):
    def test_attributes_field(self):
        field = AttributesField()
        self.assertEqual(field.verbose_name, "Attributes")
        self.assertEqual(field.blank, True)

    def test_tag_type_field(self):
        field = TagTypeField()
        self.assertEqual(field.verbose_name, "Tag type")
        self.assertEqual(field.default, "div")
        self.assertEqual(field.max_length, 255)
        self.assertEqual(
            field.help_text,
            "Select the HTML tag to be used.",
        )

        form_field = TagTypeFormField()
        self.assertEqual(
            form_field.choices,
            [
                ("div", "div"),
                ("section", "section"),
                ("article", "article"),
                ("header", "header"),
                ("footer", "footer"),
                ("aside", "aside"),
            ],
        )

    def test_optional_device_choice_field(self):
        class Form(forms.Form):
            odc = OptionalDeviceChoiceField()
            odc_not_required = OptionalDeviceChoiceField(required=False)

        form = Form(data={"odc": [size for size, _ in DEVICE_CHOICES]})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["odc"], None)

        form_1 = Form(data={"odc": ["xs", "sm"]})
        self.assertTrue(form_1.is_valid(), form_1.errors)
        self.assertEqual(form_1.cleaned_data["odc"], ["xs", "sm"])

    def test_device_choice_field(self):
        class Form(forms.Form):
            dc = DeviceChoiceField()

        class Form2(forms.Form):
            dc_not_required = DeviceChoiceField(required=False)

        form = Form(data={"dc": ["xs"]})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["dc"], ["xs"])

        form_1 = Form2(data={})
        self.assertFalse(form_1.is_valid())
        self.assertFormError(form_1, "dc_not_required", ["Please select at least one device size"])
