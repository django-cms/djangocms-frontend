from django.template import Context
from django.test import TestCase

from djangocms_frontend.contrib.icon.templatetags.icon_tags import (
    add_css_for_icon,
    icon,
)


class IconTagTestCase(TestCase):
    """Tests for the icon simple tag."""

    def test_renders_icon_html(self):
        icon_data = {"iconClass": "bi bi-star", "iconText": ""}
        result = icon(Context({}), icon_data)
        self.assertIn('<i class="bi bi-star">', result)
        self.assertIn("</i>", result)

    def test_renders_icon_with_text(self):
        icon_data = {"iconClass": "material-icons", "iconText": "home"}
        result = icon(Context({}), icon_data)
        self.assertIn("home", result)

    def test_none_icon_returns_empty(self):
        result = icon(Context({}), None)
        self.assertEqual(result, "")

    def test_empty_dict_returns_empty(self):
        result = icon(Context({}), {})
        self.assertEqual(result, "")


class AddCssForIconTagTestCase(TestCase):
    """Tests for the add_css_for_icon inclusion tag."""

    def test_adds_css_for_known_library(self):
        icon_data = {"library": "font-awesome"}
        context = Context({})
        result = add_css_for_icon(context, icon_data)
        self.assertIn("icon_css", result)
        self.assertIn("font-awesome", result["icon_css"])

    def test_no_css_for_unknown_library(self):
        icon_data = {"library": "nonexistent-library"}
        context = Context({})
        result = add_css_for_icon(context, icon_data)
        self.assertNotIn("icon_css", result)

    def test_no_css_for_none_icon(self):
        context = Context({})
        result = add_css_for_icon(context, None)
        self.assertNotIn("icon_css", result)

    def test_static_css_link(self):
        """Libraries with a filename (no slash) should get a static URL."""
        icon_data = {"library": "fomantic-ui"}
        context = Context({})
        result = add_css_for_icon(context, icon_data)
        self.assertIn("icon_css", result)
        # Should be resolved through static()
        self.assertIn("djangocms_frontend/icon/vendor", result["icon_css"])

    def test_cdn_css_link(self):
        """Libraries with a URL (containing slash) should be used as-is."""
        icon_data = {"library": "bootstrap-icons"}
        context = Context({})
        result = add_css_for_icon(context, icon_data)
        self.assertIn("icon_css", result)
        self.assertTrue(result["icon_css"].startswith("https://"))
