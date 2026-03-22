from unittest.mock import patch

from django.test import TestCase

from djangocms_frontend.contrib.grid.forms import GridColumnForm, GridContainerForm
from djangocms_frontend.contrib.grid.models import GridColumn, GridContainer, GridRow


class PluginDefaultsHierarchyTestCase(TestCase):
    """Tests for the three-level plugin defaults hierarchy:
    form field initials < model default_config < DJANGOCMS_FRONTEND_PLUGIN_DEFAULTS setting."""

    def test_form_field_defaults_are_applied(self):
        """Level 1: Form field initial values are applied by initialize_from_form."""
        instance = GridContainer.objects.create()
        instance.initialize_from_form(GridContainerForm)
        # container_type should get the form field's initial value
        self.assertEqual(instance.config["container_type"], "container")
        # spacing fields default to empty
        self.assertEqual(instance.config.get("padding_y", ""), "")

    def test_model_default_config_overrides_form_defaults(self):
        """Level 2: Model default_config overrides form field initials."""
        instance = GridContainer.objects.create()
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {
                "container_type": "container-fluid",
                "padding_y": "py-5",
            }
            instance.initialize_from_form(GridContainerForm)
            self.assertEqual(instance.config["container_type"], "container-fluid")
            self.assertEqual(instance.config["padding_y"], "py-5")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config

    @patch(
        "djangocms_frontend.models.PLUGIN_DEFAULTS",
        {
            "GridContainer": {"container_type": "container-full", "padding_x": "px-3"},
        },
    )
    def test_settings_defaults_override_form_defaults(self):
        """Level 3: PLUGIN_DEFAULTS setting overrides form field initials."""
        instance = GridContainer.objects.create()
        instance.initialize_from_form(GridContainerForm)
        self.assertEqual(instance.config["container_type"], "container-full")
        self.assertEqual(instance.config["padding_x"], "px-3")

    @patch(
        "djangocms_frontend.models.PLUGIN_DEFAULTS",
        {
            "GridContainer": {"container_type": "container-full"},
        },
    )
    def test_settings_override_model_default_config(self):
        """Level 3 beats level 2: settings override model default_config."""
        instance = GridContainer.objects.create()
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {
                "container_type": "container-fluid",
                "padding_y": "py-5",
            }
            instance.initialize_from_form(GridContainerForm)
            # Setting wins over model default_config for container_type
            self.assertEqual(instance.config["container_type"], "container-full")
            # Model default_config still applies for fields not in settings
            self.assertEqual(instance.config["padding_y"], "py-5")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config

    @patch("djangocms_frontend.models.PLUGIN_DEFAULTS", {})
    def test_unrelated_model_not_affected(self):
        """PLUGIN_DEFAULTS for one model do not affect other models."""
        instance = GridColumn.objects.create()
        instance.initialize_from_form(GridColumnForm)
        # GridColumn should only have its own form defaults
        self.assertNotIn("container_type", instance.config)

    @patch(
        "djangocms_frontend.models.PLUGIN_DEFAULTS",
        {
            "GridContainer": {"padding_y": "py-5"},
        },
    )
    def test_form_defaults_preserved_for_non_overridden_fields(self):
        """Fields not mentioned in higher layers keep their form defaults."""
        instance = GridContainer.objects.create()
        instance.initialize_from_form(GridContainerForm)
        # container_type should still have the form default
        self.assertEqual(instance.config["container_type"], "container")
        # padding_y overridden by settings
        self.assertEqual(instance.config["padding_y"], "py-5")


class GridModelTestCase(TestCase):
    def test_grid_instance(self):
        instance = GridContainer.objects.create()
        instance.initialize_from_form(GridContainerForm)
        self.assertEqual(str(instance), "GridContainer (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.config["plugin_title"] = {"show": False, "title": "test container"}
        self.assertEqual(instance.get_short_description(), "test container")

    def test_row_instance(self):
        instance = GridRow.objects.create()
        self.assertEqual(str(instance), "GridRow (1)")
        self.assertEqual(instance.get_short_description(), "(0 columns)")

    def test_column_instance(self):
        instance = GridColumn.objects.create()
        instance.initialize_from_form(GridColumnForm)
        self.assertEqual(str(instance), "GridColumn (1)")
        self.assertEqual(instance.get_short_description(), "(auto)")
        instance.config["xs_col"] = 12
        self.assertEqual(
            instance.get_short_description(),
            "(col-12)",
        )
        instance.config["md_col"] = 12
        instance.config["md_offset"] = 12
        instance.config["xs_offset"] = 12
        self.assertEqual(
            instance.get_short_description(),
            "(col-12)",
        )
        instance.config["xs_ms"] = 12
        instance.config["md_ms"] = 12
        self.assertEqual(
            instance.get_short_description(),
            "(col-12)",
        )
