from django.test import TestCase

from djangocms_frontend.contrib.content.models import (
    Blockquote, CodeBlock, Figure,
)


class B5ContentModelTestCase(TestCase):

    def test_code_instance(self):
        instance = CodeBlock.objects.create()
        self.assertEqual(str(instance), "CodeBlock (1)")
        self.assertEqual(instance.get_short_description(), "<code>")

    def test_blockquote_instance(self):
        instance = Blockquote.objects.create()
        self.assertEqual(str(instance), "Blockquote (1)")
        self.assertEqual(instance.get_short_description(), "")

    def test_figure_instance(self):
        instance = Figure.objects.create()
        self.assertEqual(str(instance), "Figure (1)")
        self.assertEqual(instance.get_short_description(), "")
