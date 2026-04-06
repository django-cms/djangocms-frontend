from io import StringIO
from unittest.mock import patch

from cms.models import CMSPlugin
from django.core.management import call_command
from django.test import TestCase

from djangocms_frontend.contrib.alert.models import Alert


class RenameCommandTestCase(TestCase):
    """Tests for the frontend rename management command."""

    def _call_rename(self, old, new, **kwargs):
        out = StringIO()
        err = StringIO()
        call_command("frontend", "rename", old, new, stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()

    def test_rename_updates_plugin_type(self):
        """Renaming updates plugin_type on all matching CMSPlugin rows."""
        instance = Alert.objects.create(
            config=dict(alert_context="primary"),
        )
        # Simulate an old, uninstalled plugin type
        CMSPlugin.objects.filter(pk=instance.pk).update(plugin_type="OldAlertPlugin")

        out, err = self._call_rename("OldAlertPlugin", "AlertPlugin")

        instance.refresh_from_db()
        self.assertEqual(instance.plugin_type, "AlertPlugin")
        self.assertIn("Updated", out)
        self.assertEqual(err, "")

    def test_rename_updates_ui_item(self):
        """If new plugin model is an AbstractFrontendUIItem subclass, ui_item is updated."""
        instance = Alert.objects.create(
            config=dict(alert_context="primary"),
        )
        CMSPlugin.objects.filter(pk=instance.pk).update(plugin_type="OldAlertPlugin")
        Alert.objects.filter(pk=instance.pk).update(ui_item="OldAlert")

        out, _ = self._call_rename("OldAlertPlugin", "AlertPlugin")

        instance.refresh_from_db()
        self.assertEqual(instance.ui_item, "Alert")
        self.assertIn("ui_item", out)

    def test_rename_does_not_touch_other_plugins(self):
        """Only plugins with the old plugin_type are affected."""
        instance1 = Alert.objects.create(config=dict(alert_context="primary"))
        instance2 = Alert.objects.create(config=dict(alert_context="danger"))
        CMSPlugin.objects.filter(pk=instance1.pk).update(plugin_type="OldAlertPlugin")
        CMSPlugin.objects.filter(pk=instance2.pk).update(plugin_type="AlertPlugin")

        self._call_rename("OldAlertPlugin", "AlertPlugin")

        instance1.refresh_from_db()
        instance2.refresh_from_db()
        self.assertEqual(instance1.plugin_type, "AlertPlugin")
        self.assertEqual(instance2.plugin_type, "AlertPlugin")
        # Only 1 was renamed, not 2
        self.assertEqual(instance2.config["alert_context"], "danger")

    def test_rename_multiple_plugins(self):
        """All instances with the old plugin_type are renamed."""
        instances = [Alert.objects.create(config=dict(alert_context="primary")) for _ in range(3)]
        pks = [i.pk for i in instances]
        CMSPlugin.objects.filter(pk__in=pks).update(plugin_type="OldAlertPlugin")

        out, _ = self._call_rename("OldAlertPlugin", "AlertPlugin")

        for pk in pks:
            self.assertEqual(CMSPlugin.objects.get(pk=pk).plugin_type, "AlertPlugin")
        self.assertIn("Updated 3 plugins", out)

    def test_error_old_plugin_still_installed(self):
        """Renaming fails if old_plugin is still installed."""
        Alert.objects.create(config=dict(alert_context="primary"))

        _, err = self._call_rename("AlertPlugin", "AlertPlugin")

        self.assertIn("still installed", err)

    def test_error_old_plugin_not_in_db(self):
        """Renaming fails if old_plugin has no rows in the database."""
        _, err = self._call_rename("GhostPlugin", "AlertPlugin")

        self.assertIn("not found in the database", err)

    def test_error_new_plugin_not_installed(self):
        """Renaming fails if new_plugin is not installed."""
        instance = Alert.objects.create(config=dict(alert_context="primary"))
        CMSPlugin.objects.filter(pk=instance.pk).update(plugin_type="OldAlertPlugin")

        _, err = self._call_rename("OldAlertPlugin", "NonExistentPlugin")

        self.assertIn("not installed", err)
        # Verify nothing changed
        instance.refresh_from_db()
        self.assertEqual(instance.plugin_type, "OldAlertPlugin")

    def test_ui_item_not_updated_when_already_correct(self):
        """No ui_item update is reported when ui_item already matches."""
        instance = Alert.objects.create(config=dict(alert_context="primary"))
        # ui_item is "Alert" by default (set in save()), plugin_type is "AlertPlugin"
        CMSPlugin.objects.filter(pk=instance.pk).update(plugin_type="OldAlertPlugin")
        # ui_item is already "Alert" which matches the new plugin's model name

        out, _ = self._call_rename("OldAlertPlugin", "AlertPlugin")

        self.assertIn("Updated 1 plugins", out)
        self.assertNotIn("ui_item", out)

    def test_warning_for_non_frontend_plugin(self):
        """A warning is shown when renaming to a non-AbstractFrontendUIItem plugin."""
        CMSPlugin.objects.create(plugin_type="OldTextPlugin")

        out, _ = self._call_rename("OldTextPlugin", "TextPlugin", interactive=False)

        self.assertIn("not based on AbstractFrontendUIItem", out)
        self.assertIn("Updated 1 plugins", out)

    @patch("builtins.input", return_value="no")
    def test_aborts_when_user_declines_non_frontend_rename(self, mock_input):
        """Renaming to a non-AbstractFrontendUIItem plugin aborts if user declines."""
        instance = CMSPlugin.objects.create(plugin_type="OldTextPlugin")

        out, _ = self._call_rename("OldTextPlugin", "TextPlugin")

        self.assertIn("not based on AbstractFrontendUIItem", out)
        self.assertIn("Aborted", out)
        instance.refresh_from_db()
        self.assertEqual(instance.plugin_type, "OldTextPlugin")

    @patch("builtins.input", return_value="yes")
    def test_proceeds_when_user_confirms_non_frontend_rename(self, mock_input):
        """Renaming to a non-AbstractFrontendUIItem plugin proceeds if user confirms."""
        instance = CMSPlugin.objects.create(plugin_type="OldTextPlugin")

        out, _ = self._call_rename("OldTextPlugin", "TextPlugin")

        self.assertIn("Updated 1 plugins", out)
        instance.refresh_from_db()
        self.assertEqual(instance.plugin_type, "TextPlugin")

    def test_no_warning_for_frontend_plugin(self):
        """No warning is shown when renaming to an AbstractFrontendUIItem plugin."""
        instance = Alert.objects.create(config=dict(alert_context="primary"))
        CMSPlugin.objects.filter(pk=instance.pk).update(plugin_type="OldAlertPlugin")

        out, _ = self._call_rename("OldAlertPlugin", "AlertPlugin")

        self.assertNotIn("not based on AbstractFrontendUIItem", out)
        self.assertIn("Updated 1 plugins", out)

    @patch(
        "djangocms_frontend.management.commands.subcommands.rename.plugin_pool.get_all_plugins",
    )
    def test_rename_to_plugin_with_no_model(self, mock_get_all):
        """Renaming to a plugin with model=None works without warning or confirmation."""
        # Create a fake plugin class with no model
        fake_plugin = type("NoModelPlugin", (), {"__name__": "NoModelPlugin", "model": None})
        mock_get_all.return_value = [fake_plugin]

        CMSPlugin.objects.create(plugin_type="OldPlugin")

        out, _ = self._call_rename("OldPlugin", "NoModelPlugin")

        self.assertNotIn("not based on AbstractFrontendUIItem", out)
        self.assertNotIn("Aborted", out)
        self.assertIn("Updated 1 plugins", out)
        self.assertNotIn("ui_item", out)
