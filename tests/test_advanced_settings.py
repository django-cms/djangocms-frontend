from io import StringIO
from unittest.mock import patch

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.core.management import call_command
from django.test import TestCase

from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm
from djangocms_frontend.contrib.alert.models import Alert

from .fixtures import TestFixture


class AdvancedSettingsModelTestCase(TestCase):
    """Tests for get_attributes/get_classes/tag_type when SHOW_ADVANCED_SETTINGS is False."""

    def test_get_attributes_includes_user_attributes_by_default(self):
        instance = Alert.objects.create(
            config=dict(attributes={"data-test": "value", "class": "custom-class"}),
        )
        instance.initialize_from_form(AlertForm).save()
        attrs = instance.get_attributes()
        self.assertIn("data-test", attrs)
        self.assertIn("custom-class", attrs)

    def test_get_classes_includes_user_classes_by_default(self):
        instance = Alert.objects.create(
            config=dict(attributes={"class": "custom-class"}),
        )
        instance.initialize_from_form(AlertForm).save()
        classes = instance.get_classes()
        self.assertIn("custom-class", classes)

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_get_attributes_excludes_user_attributes_when_disabled(self):
        instance = Alert.objects.create(
            config=dict(attributes={"data-test": "value", "class": "custom-class"}),
        )
        instance.initialize_from_form(AlertForm).save()
        attrs = instance.get_attributes()
        self.assertNotIn("data-test", attrs)
        self.assertNotIn("custom-class", attrs)

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_get_classes_excludes_user_classes_when_disabled(self):
        instance = Alert.objects.create(
            config=dict(attributes={"class": "custom-class"}),
        )
        instance.initialize_from_form(AlertForm).save()
        classes = instance.get_classes()
        self.assertNotIn("custom-class", classes)

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_programmatic_classes_still_rendered_when_disabled(self):
        instance = Alert.objects.create(
            config=dict(attributes={"class": "custom-class"}),
        )
        instance.initialize_from_form(AlertForm).save()
        instance.add_classes("programmatic-class")
        classes = instance.get_classes()
        self.assertIn("programmatic-class", classes)
        self.assertNotIn("custom-class", classes)

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_tag_type_reset_to_default_when_disabled(self):
        instance = Alert.objects.create(tag_type="section")
        instance.initialize_from_form(AlertForm).save()
        self.assertEqual(instance.tag_type, "div")

    def test_tag_type_preserved_when_enabled(self):
        instance = Alert.objects.create(tag_type="section")
        instance.initialize_from_form(AlertForm).save()
        self.assertEqual(instance.tag_type, "section")


class AdvancedSettingsFieldsetTestCase(TestFixture, CMSTestCase):
    """Tests for the admin fieldset visibility."""

    def test_fieldset_shown_by_default(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(AlertForm).save()

        admin = AlertPlugin()
        fieldsets = admin.get_fieldsets(request=None, obj=plugin)
        fieldset_names = [name for name, _ in fieldsets]
        self.assertIn("Advanced settings", fieldset_names)

    @patch("djangocms_frontend.common.attributes.SHOW_ADVANCED_SETTINGS", False)
    def test_fieldset_hidden_when_disabled(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(AlertForm).save()

        admin = AlertPlugin()
        fieldsets = admin.get_fieldsets(request=None, obj=plugin)
        fieldset_names = [name for name, _ in fieldsets]
        self.assertNotIn("Advanced settings", fieldset_names)


class AdvancedSettingsRenderTestCase(TestFixture, CMSTestCase):
    """Tests that advanced settings are not rendered in templates when disabled."""

    def test_user_attributes_rendered_by_default(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(attributes={"data-custom": "hello"}),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-custom="hello"')

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_user_attributes_not_rendered_when_disabled(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            config=dict(attributes={"data-custom": "hello"}),
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'data-custom="hello"')

    @patch("djangocms_frontend.models.SHOW_ADVANCED_SETTINGS", False)
    def test_custom_tag_type_not_rendered_when_disabled(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
            tag_type="section",
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<section")
        self.assertContains(response, "<div")


class ClearAdvancedSettingsCommandTestCase(TestCase):
    """Tests for the clear_advanced_settings management command."""

    def test_clears_attributes_and_tag_type(self):
        instance = Alert.objects.create(
            tag_type="section",
            config=dict(
                alert_context="primary",
                alert_dismissible=False,
                attributes={"data-test": "value", "class": "custom"},
            ),
        )

        out = StringIO()
        call_command("frontend", "clear_advanced_settings", "--noinput", stdout=out)

        instance.refresh_from_db()
        self.assertEqual(instance.config.get("attributes"), {})
        self.assertEqual(instance.tag_type, "div")
        self.assertIn("Done", out.getvalue())

    def test_preserves_other_config(self):
        instance = Alert.objects.create(
            config=dict(
                alert_context="danger",
                alert_dismissible=True,
                attributes={"data-test": "value"},
            ),
        )

        out = StringIO()
        call_command("frontend", "clear_advanced_settings", "--noinput", stdout=out)

        instance.refresh_from_db()
        self.assertEqual(instance.config["alert_context"], "danger")
        self.assertTrue(instance.config["alert_dismissible"])

    def test_noop_when_no_advanced_settings(self):
        Alert.objects.create(
            config=dict(alert_context="primary", attributes={}),
        )

        out = StringIO()
        call_command("frontend", "clear_advanced_settings", "--noinput", stdout=out)

        output = out.getvalue()
        self.assertIn("Cleared attributes on 0 plugin(s)", output)
        self.assertIn("reset tag_type on 0 plugin(s)", output)

    def test_counts_are_correct(self):
        Alert.objects.create(
            tag_type="section",
            config=dict(attributes={"class": "foo"}),
        )
        Alert.objects.create(
            tag_type="div",
            config=dict(attributes={"data-x": "y"}),
        )
        Alert.objects.create(
            tag_type="article",
            config=dict(attributes={}),
        )

        out = StringIO()
        call_command("frontend", "clear_advanced_settings", "--noinput", stdout=out)

        output = out.getvalue()
        self.assertIn("Cleared attributes on 2 plugin(s)", output)
        self.assertIn("reset tag_type on 2 plugin(s)", output)
