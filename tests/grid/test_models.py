from unittest.mock import patch

from django.test import RequestFactory, TestCase

from djangocms_frontend.contrib.grid.cms_plugins import GridContainerPlugin
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


class GetFormDefaultsTestCase(TestCase):
    """Tests that get_form applies default_config and PLUGIN_DEFAULTS as field initials."""

    def _get_form_instance(self, plugin_cls):
        """Helper to get an instantiated form from a plugin's get_form (add mode)."""
        request = RequestFactory().get("/")
        plugin = plugin_cls()
        form_cls = plugin.get_form(request, obj=None, change=False)
        return form_cls()

    def test_no_defaults_returns_original_form(self):
        """Without any defaults, get_form returns the original form class."""
        request = RequestFactory().get("/")
        plugin = GridContainerPlugin()
        form_cls = plugin.get_form(request, obj=None, change=False)
        self.assertEqual(form_cls.__name__, GridContainerForm.__name__)

    def test_model_default_config_sets_initial(self):
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {"container_type": "container-fluid"}
            form = self._get_form_instance(GridContainerPlugin)
            self.assertEqual(form.fields["container_type"].initial, "container-fluid")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config

    @patch(
        "djangocms_frontend.ui_plugin_base.PLUGIN_DEFAULTS",
        {"GridContainer": {"container_type": "container-full"}},
    )
    def test_plugin_defaults_setting_sets_initial(self):
        form = self._get_form_instance(GridContainerPlugin)
        self.assertEqual(form.fields["container_type"].initial, "container-full")

    @patch(
        "djangocms_frontend.ui_plugin_base.PLUGIN_DEFAULTS",
        {"GridContainer": {"container_type": "from-settings"}},
    )
    def test_settings_override_model_default_config_in_form(self):
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {"container_type": "from-model"}
            form = self._get_form_instance(GridContainerPlugin)
            self.assertEqual(form.fields["container_type"].initial, "from-settings")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config

    def test_default_config_does_not_leak_to_other_plugins(self):
        """Regression: setting default_config on one plugin must not affect other plugins
        sharing the same form field instances (e.g. SpacingFormMixin fields)."""
        from djangocms_frontend.contrib.link.cms_plugins import TextLinkPlugin

        # Set a default_config on GridContainer that affects a shared field
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {"padding_y": "py-6"}
            # Trigger get_form on GridContainer to apply the default
            self._get_form_instance(GridContainerPlugin)
            # Now get the Link form — padding_y should NOT have the GridContainer default
            link_form = self._get_form_instance(TextLinkPlugin)
            self.assertNotEqual(link_form.fields["padding_y"].initial, "py-6")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config

    def test_change_form_does_not_override_initials(self):
        """On edit (change=True), defaults should NOT be applied."""
        original = getattr(GridContainer, "default_config", {})
        try:
            GridContainer.default_config = {"container_type": "container-fluid"}
            request = RequestFactory().get("/")
            plugin = GridContainerPlugin()
            form_cls = plugin.get_form(request, obj=None, change=True)
            form = form_cls()
            # Should have the original form field initial, not the default_config value
            self.assertNotEqual(form.fields["container_type"].initial, "container-fluid")
        finally:
            if original:
                GridContainer.default_config = original
            else:
                del GridContainer.default_config


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
