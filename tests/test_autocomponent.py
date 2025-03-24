from cms.api import add_plugin
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

    def test_render_autocomponent(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type="AutoHeroPlugin",
            language=self.language,
            config={"title": "My Hero", "slogan": "My Hero Slogan", "hero_image": None},
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

        # Declarative tags render empty
        self.assertContains(response, 9 * "\n" + '<section class="bg-white dark:bg-gray-900">')
        self.assertContains(response, "My Hero")
        self.assertContains(response, "My Hero Slogan")

    def test_split_template_tag(self):
        from djangocms_frontend.templatetags.cms_component import split

        self.assertEqual(split("hero.html"), ["hero.html"])
        self.assertEqual(split("Mixin1|Mixin2"), ["Mixin1", "Mixin2"])
        self.assertEqual(split("hero.html"), ["hero.html"])
        self.assertEqual(split("hero.html, Mixin1, Mixin2", ", "), ["hero.html", "Mixin1", "Mixin2"])

    def test_autocomponents_slots_are_created(self):
        from cms.plugin_pool import plugin_pool

        self.assertIn("AutoHeroWithSlotsPlugin", plugin_pool.plugins)

        plugin = plugin_pool.get_plugin("AutoHeroWithSlotsPlugin")
        model = plugin.model

        self.assertEqual(model.__name__, "AutoHeroWithSlots")
        self.assertTrue(plugin.allow_children)
        self.assertEqual(plugin.child_classes, ["AutoHeroWithSlotsButtonsPlugin"])

        self.assertIn("AutoHeroWithSlotsButtonsPlugin", plugin_pool.plugins)
        slot_plugin = plugin_pool.get_plugin("AutoHeroWithSlotsButtonsPlugin")

        self.assertEqual(slot_plugin.parent_classes, ["AutoHeroWithSlotsPlugin"])
