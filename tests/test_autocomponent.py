from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.template import Template, TemplateSyntaxError

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
        self.assertIn("title", form.declared_fields)
        self.assertIn("slogan", form.declared_fields)
        self.assertIn("hero_image", form.declared_fields)
        self.assertIn("config", form.declared_fields)  # Inherited from djangocms_frontend.models.FrontendUIItem

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

    def test_autocomponents_slots_are_created(self):
        from cms.plugin_pool import plugin_pool

        self.assertIn("AutoHeroWithSlotsPlugin", plugin_pool.plugins)

        plugin = plugin_pool.get_plugin("AutoHeroWithSlotsPlugin")
        model = plugin.model
        form = plugin.form
        self.assertEqual(model.__name__, "AutoHeroWithSlots")
        self.assertIn("title", form.declared_fields)
        self.assertIn("slogan", form.declared_fields)
        self.assertIn("hero_image", form.declared_fields)
        self.assertIn("config", form.declared_fields)  # Inherited from djangocms_frontend.models.FrontendUIItem
        self.assertTrue(plugin.allow_children)
        self.assertEqual(plugin.child_classes, ["AutoHeroWithSlotsButtonsPlugin"])

        self.assertIn("AutoHeroWithSlotsButtonsPlugin", plugin_pool.plugins)
        slot_plugin = plugin_pool.get_plugin("AutoHeroWithSlotsButtonsPlugin")

        self.assertEqual(slot_plugin.parent_classes, ["AutoHeroWithSlotsPlugin"])

    def test_split_template_tag(self):
        from djangocms_frontend.templatetags.cms_component import split

        self.assertEqual(split("hero.html"), ["hero.html"])
        self.assertEqual(split("Mixin1|Mixin2"), ["Mixin1", "Mixin2"])
        self.assertEqual(split("hero.html"), ["hero.html"])
        self.assertEqual(split("hero.html, Mixin1, Mixin2", ", "), ["hero.html", "Mixin1", "Mixin2"])

    def test_invalid_cms_component_usage_missing_required_argument(self):
        # The {% cms_component %} tag requires a component name.
        invalid_template = "{% load cms_tags %}{% cms_component %}"
        with self.assertRaises(TemplateSyntaxError):
            Template(invalid_template)

    def test_invalid_field_usage_invalid_argument(self):
        # The {% field %} tag requires valid arguments: a field name and a component instance.
        # Here we simulate invalid usage by providing an invalid component.
        invalid_template = "{% load cms_tags %}{% field 'nonexistent_field' component %}"
        with self.assertRaises(TemplateSyntaxError):
            Template(invalid_template)

    def test_multiple_cms_component_tags_error(self):
        # Assuming only one {% cms_component %} tag is allowed per template.
        # This should raise an error if multiple tags are used.
        invalid_template = "{% load cms_tags %}{% cms_component 'Hero' %}{% cms_component 'Footer' %}"
        with self.assertRaises(TemplateSyntaxError):
            Template(invalid_template)
