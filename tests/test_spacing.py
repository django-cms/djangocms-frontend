from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.core.exceptions import ValidationError
from django.test import TestCase

from djangocms_frontend.common.bootstrap5.spacing import (
    SpacingSizeSideField,
    get_spacing_classes,
)
from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm

from .fixtures import TestFixture


class GetSpacingClassesTestCase(TestCase):
    """Tests for get_spacing_classes utility function."""

    def test_basic_spacing(self):
        result = get_spacing_classes(["mx-3", "my-2"])
        self.assertEqual(result, ["mx-3", "my-2"])

    def test_filters_empty_size(self):
        """Entries ending with '-' (no size selected) should be filtered out."""
        result = get_spacing_classes(["mx-3", "my-"])
        self.assertEqual(result, ["mx-3"])

    def test_empty_input(self):
        self.assertEqual(get_spacing_classes([]), [])

    def test_with_all_devices(self):
        """When active_set covers all devices, same as default behavior."""
        result = get_spacing_classes(
            ["mx-3"],
            active_set={"xs", "sm", "md", "lg", "xl", "xxl"},
        )
        self.assertEqual(result, ["mx-3"])

    def test_with_subset_of_devices(self):
        """When only some devices are active, responsive classes are generated."""
        result = get_spacing_classes(["mx-3"], active_set={"xs", "sm"})
        self.assertIn("mx-3", result)
        # Should add a zero-out class for the first non-active breakpoint
        self.assertTrue(
            any("md" in cls for cls in result),
            f"Expected responsive md class in {result}",
        )

    def test_with_no_xs_device(self):
        """When xs is not in active set, spacing shouldn't apply at xs."""
        result = get_spacing_classes(["mx-3"], active_set={"md", "lg"})
        self.assertTrue(len(result) > 0, "Expected responsive classes")


class SpacingSizeSideFieldTestCase(TestCase):
    """Tests for SpacingSizeSideField form field."""

    def _make_field(self):
        from djangocms_frontend import settings

        return SpacingSizeSideField(
            property="m",
            size_choices=settings.SPACER_SIZE_CHOICES,
            side_choices=settings.SPACER_X_SIDES_CHOICES,
        )

    def test_compress_with_size(self):
        field = self._make_field()
        result = field.compress(["mx", "3"])
        self.assertEqual(result, "mx-3")

    def test_compress_without_size(self):
        field = self._make_field()
        result = field.compress(["mx", ""])
        self.assertEqual(result, "")

    def test_compress_empty(self):
        field = self._make_field()
        result = field.compress([])
        self.assertEqual(result, "")

    def test_clean_valid(self):
        field = self._make_field()
        result = field.clean(["mx", "3"])
        self.assertEqual(result, "mx-3")

    def test_clean_size_without_side_raises(self):
        field = self._make_field()
        with self.assertRaises(ValidationError):
            field.clean(["", "3"])

    def test_clean_empty_is_valid(self):
        field = self._make_field()
        result = field.clean(["", ""])
        self.assertEqual(result, "")

    def test_clean_none_is_valid(self):
        field = self._make_field()
        result = field.clean(None)
        self.assertEqual(result, "")


class SpacingRenderTestCase(TestFixture, CMSTestCase):
    """Tests that spacing classes are rendered in plugin output."""

    def test_margin_classes_rendered(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(margin_x="mx-3", margin_y="my-2"),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("mx-3", content)
        self.assertIn("my-2", content)

    def test_padding_classes_rendered(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(padding_x="px-4", padding_y="py-1"),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("px-4", content)
        self.assertIn("py-1", content)

    def test_spacing_with_device_restriction(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(
                margin_x="mx-3",
                margin_devices=["xs", "sm"],
            ),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("mx-3", content)
