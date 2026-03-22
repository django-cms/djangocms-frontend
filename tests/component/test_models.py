from unittest.mock import patch

from django.test import TestCase

from djangocms_frontend.component_pool import components


class ComponentPluginTestCase(TestCase):
    def test_component_description(self):
        MyHero, MyHeroPlugin, _ = components["MyHero"]

        instance = MyHero.objects.create()
        instance.initialize_from_form(MyHeroPlugin.form)

        self.assertEqual(instance.get_short_description(), "my title")


class ComponentDefaultConfigTestCase(TestCase):
    """Tests that default_config in a component's Meta class is applied to the generated model."""

    def test_meta_default_config_is_set_on_model(self):
        """The generated proxy model has the default_config from Meta."""
        MyDefaultsComponent, _, _ = components["MyDefaultsComponent"]
        self.assertEqual(
            MyDefaultsComponent.default_config,
            {"title": "Default Title", "color": "primary"},
        )

    def test_default_config_overrides_form_initials(self):
        """Meta default_config overrides form field initial values."""
        MyDefaultsComponent, MyDefaultsComponentPlugin, _ = components["MyDefaultsComponent"]
        instance = MyDefaultsComponent.objects.create()
        instance.initialize_from_form(MyDefaultsComponentPlugin.form)
        # default_config overrides form initials
        self.assertEqual(instance.config["title"], "Default Title")
        self.assertEqual(instance.config["color"], "primary")
        # Fields not in default_config keep form initials
        self.assertEqual(instance.config["extra"], "form-extra")

    @patch(
        "djangocms_frontend.models.PLUGIN_DEFAULTS",
        {
            "MyDefaultsComponent": {"title": "Settings Title"},
        },
    )
    def test_settings_override_meta_default_config(self):
        """PLUGIN_DEFAULTS setting overrides Meta default_config."""
        MyDefaultsComponent, MyDefaultsComponentPlugin, _ = components["MyDefaultsComponent"]
        instance = MyDefaultsComponent.objects.create()
        instance.initialize_from_form(MyDefaultsComponentPlugin.form)
        # Settings win over Meta default_config
        self.assertEqual(instance.config["title"], "Settings Title")
        # Meta default_config still applies for fields not in settings
        self.assertEqual(instance.config["color"], "primary")
        # Form initials still apply for fields not in either
        self.assertEqual(instance.config["extra"], "form-extra")

    def test_component_without_default_config(self):
        """Components without default_config in Meta work normally."""
        MyHero, MyHeroPlugin, _ = components["MyHero"]
        self.assertFalse(hasattr(MyHero, "default_config"))
        instance = MyHero.objects.create()
        instance.initialize_from_form(MyHeroPlugin.form)
        self.assertEqual(instance.config["title"], "my title")
