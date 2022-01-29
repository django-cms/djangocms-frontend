from django.test import TestCase

from djangocms_frontend.fields import AttributesField, TagTypeField


class FieldsTestCase(TestCase):
    def test_attributes_field(self):
        field = AttributesField()
        self.assertEqual(field.verbose_name, "Attributes")
        self.assertEqual(field.blank, True)

    def test_tag_type_field(self):
        field = TagTypeField()
        self.assertEqual(field.verbose_name, "Tag type")
        self.assertEqual(
            field.choices,
            (
                ("div", "div"),
                ("section", "section"),
                ("article", "article"),
                ("header", "header"),
                ("footer", "footer"),
                ("aside", "aside"),
            ),
        )
        self.assertEqual(field.default, "div")
        self.assertEqual(field.max_length, 255)
        self.assertEqual(
            field.help_text,
            "Select the HTML tag to be used.",
        )
