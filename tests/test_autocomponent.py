from cms.test_utils.testcases import CMSTestCase

from tests.fixtures import TestFixture


class AutoComponentTestCase(TestFixture, CMSTestCase):
    def test_autocomponents_are_auto_detected(self):
        from cms.plugin_pool import plugin_pool

        self.assertIn("AutoHeroPlugin", plugin_pool.plugins)

        plugin = plugin_pool.get_plugin("AutoHeroPlugin")
        model = plugin.model
        form = plugin.form

        self.assertEqual(plugin.name, "My Hero Auto Component")
        self.assertEqual(model.__name__, "AutoHero")
        self.assertIn("title", form.base_fields)
        self.assertIn("slogan", form.base_fields)
        self.assertIn("hero_image", form.base_fields)
        self.assertIn("config", form.base_fields)  # Inherited from djangocms_frontend.models.FrontendUIItem

        self.assertTrue(plugin.allow_children)
