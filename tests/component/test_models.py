from django.test import TestCase

from djangocms_frontend.component_pool import components


class ComponentPluginTestCase(TestCase):
    def test_component_description(self):
        MyHero, MyHeroPlugin, _ = components["MyHero"]

        instance = MyHero.objects.create()
        instance.initialize_from_form(MyHeroPlugin.form)

        self.assertEqual(instance.get_short_description(), "my title")
