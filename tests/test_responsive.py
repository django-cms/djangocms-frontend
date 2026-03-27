from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.test import TestCase

from djangocms_frontend.common.bootstrap5.responsive import get_display_classes
from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm

from .fixtures import TestFixture


class GetDisplayClassesTestCase(TestCase):
    """Tests for get_display_classes utility function."""

    def test_all_devices_visible_returns_empty(self):
        """If all devices are visible, no display classes needed."""
        result = get_display_classes({"xs", "sm", "md", "lg", "xl", "xxl"})
        self.assertEqual(result, [])

    def test_no_devices_visible_returns_none(self):
        """If no devices are visible, should get d-none at xs."""
        result = get_display_classes(set())
        self.assertIn("d-none", result)

    def test_hide_on_small_only(self):
        """Visible on xs, hidden on sm, visible again on md+."""
        result = get_display_classes({"xs", "md", "lg", "xl", "xxl"})
        self.assertIn("d-sm-none", result)
        self.assertIn("d-md-block", result)

    def test_only_mobile(self):
        """Only visible on xs and sm."""
        result = get_display_classes({"xs", "sm"})
        self.assertIn("d-md-none", result)
        self.assertNotIn("d-none", result)

    def test_only_desktop(self):
        """Only visible on lg and above."""
        result = get_display_classes({"lg", "xl", "xxl"})
        self.assertIn("d-none", result)
        self.assertIn("d-lg-block", result)

    def test_custom_visibility_class(self):
        """Test with flex instead of block (e.g. for GridRow)."""
        result = get_display_classes({"lg", "xl", "xxl"}, visibility_class="flex")
        self.assertIn("d-none", result)
        self.assertIn("d-lg-flex", result)

    def test_single_device(self):
        """Only visible on md."""
        result = get_display_classes({"md"})
        self.assertIn("d-none", result)
        self.assertIn("d-md-block", result)
        self.assertIn("d-lg-none", result)


class ResponsiveRenderTestCase(TestFixture, CMSTestCase):
    """Tests that responsive visibility classes are rendered."""

    def test_responsive_visibility_rendered(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(responsive_visibility=["xs", "sm"]),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("d-md-none", content)

    def test_no_responsive_visibility_no_display_classes(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertNotIn("d-none", content)
        self.assertNotIn("d-sm-", content)
