"""HTML config fields must be sanitized by ``clean()`` -- not only by the admin form --
so instances built outside the editing form (imports, programmatic creation, the API)
cannot carry unsanitized markup that the render-side filters later ``mark_safe``."""

from django.test import TestCase

from djangocms_frontend.contrib.content.models import Blockquote
from djangocms_frontend.fields import HTMLsanitized


class HTMLConfigSanitizationTestCase(TestCase):
    def _blockquote(self, **config):
        return Blockquote(plugin_type="BlockquotePlugin", config=config)

    def test_html_fields_are_detected(self):
        instance = self._blockquote()
        self.assertEqual(instance._html_config_fields(), frozenset({"quote_content", "quote_origin"}))

    def test_clean_strips_script_from_html_field(self):
        instance = self._blockquote(quote_content="<p>hi</p><script>alert('xss')</script>")
        instance.clean()
        self.assertNotIn("<script", instance.config["quote_content"])
        self.assertIn("hi", instance.config["quote_content"])

    def test_clean_strips_dangerous_attributes(self):
        instance = self._blockquote(quote_content="<img src=x onerror=alert(1)>")
        instance.clean()
        self.assertNotIn("onerror", instance.config["quote_content"])

    def test_clean_neutralizes_javascript_href(self):
        instance = self._blockquote(quote_content='<a href="javascript:alert(1)">x</a>')
        instance.clean()
        self.assertNotIn("javascript:", instance.config["quote_content"])

    def test_clean_leaves_safe_html_untouched(self):
        safe = "<p>Hello <strong>world</strong></p>"
        instance = self._blockquote(quote_content=safe)
        instance.clean()
        self.assertEqual(instance.config["quote_content"], safe)

    def test_clean_is_idempotent(self):
        instance = self._blockquote(quote_content="<p>hi</p><script>x</script>")
        instance.clean()
        once = instance.config["quote_content"]
        instance.clean()
        self.assertEqual(instance.config["quote_content"], once)

    def test_non_html_fields_are_not_rewritten(self):
        instance = self._blockquote(quote_alignment="text-start")
        instance.clean()
        self.assertEqual(instance.config["quote_alignment"], "text-start")

    def test_empty_and_missing_html_fields_are_safe(self):
        instance = self._blockquote(quote_content="")
        instance.clean()  # must not raise
        self.assertEqual(instance.config["quote_content"], "")


class HTMLSanitizationToggleTestCase(TestCase):
    def test_sanitizer_available_in_test_environment(self):
        # The suite runs with djangocms_text installed; the guard reflects that.
        self.assertTrue(HTMLsanitized)
