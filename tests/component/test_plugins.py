from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.cms_plugins import (
    MyButtonPlugin,
    MyCardWithFieldsetsPlugin,
    MyHeroPlugin,
    MyStrangeComponentPlugin,
)
from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin

from ..fixtures import TestFixture


class ComponentPluginTestCase(TestFixture, CMSTestCase):
    def test_component_with_empty_slots_plugin(self):
        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=MyHeroPlugin.__name__,
            language=self.language,
        )
        instance.initialize_from_form(MyHeroPlugin.form).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        # Default title is rendered in a formatted h1 tag
        self.assertInHTML(
            '<h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight '
            'leading-none md:text-5xl xl:text-6xl dark:text-white">my title</h1>',
            response.content.decode("utf-8"),
        )
        # Default slogan
        self.assertInHTML(
            '<p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl '
            'dark:text-gray-400">'
            "django CMS' plugins are great components"
            "</p>",
            response.content.decode("utf-8"),
        )
        # Default slot content
        self.assertInHTML(
            '<a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 '
            "text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 "
            'focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">'
            "Get started"
            '<svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" '
            'xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" '
            'd="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 '
            '1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>'
            "</a>",
            response.content.decode("utf-8"),
        )

    def test_component_with_slots_plugin(self):
        from djangocms_frontend.cms_plugins import MyHeroSlotPlugin

        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=MyHeroPlugin.__name__,
            language=self.language,
        )
        instance.initialize_from_form(MyHeroPlugin.form).save()
        slot = add_plugin(
            placeholder=self.placeholder,
            target=instance,
            plugin_type=MyHeroSlotPlugin.__name__,
            language=self.language,
        )
        add_plugin(
            placeholder=self.placeholder,
            target=slot,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        ).initialize_from_form(AlertPlugin.form).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)

        # Default title is rendered in a formatted h1 tag
        self.assertInHTML(
            '<h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight '
            'leading-none md:text-5xl xl:text-6xl dark:text-white">my title</h1>',
            response.content.decode("utf-8"),
        )
        # Default slogan
        self.assertInHTML(
            '<p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl '
            'dark:text-gray-400">'
            "django CMS' plugins are great components"
            "</p>",
            response.content.decode("utf-8"),
            count=1,
        )

        # Slot content is present
        self.assertInHTML(
            '<div class="alert alert-primary" role="alert"><div></div></div>',
            response.content.decode("utf-8"),
            count=1,
        )
        # Default slot content not present
        self.assertInHTML(
            '<a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 '
            "text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 "
            'focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">'
            "Get started"
            '<svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" '
            'xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" '
            'd="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 '
            '1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>'
            "</a>",
            response.content.decode("utf-8"),
            count=0,
        )

    def test_autocreate_slots(self):
        from djangocms_frontend.cms_plugins import MyHeroSlotPlugin, MyHeroTitlePlugin

        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=MyHeroPlugin.__name__,
            language=self.language,
        )
        request = self.get_request(path="/")
        MyHeroPlugin().save_model(request=request, obj=instance, form=MyHeroPlugin.form, change=False)

        plugins = list(self.placeholder.get_plugins())

        self.assertEqual(len(plugins), 3)
        self.assertEqual(plugins[0].plugin_type, MyHeroPlugin.__name__)
        self.assertIsNone(plugins[0].parent)
        self.assertEqual(plugins[1].plugin_type, MyHeroTitlePlugin.__name__)
        self.assertEqual(plugins[1].parent.pk, instance.pk)
        self.assertEqual(plugins[2].plugin_type, MyHeroSlotPlugin.__name__)
        self.assertEqual(plugins[2].parent.pk, instance.pk)

    def test_simple_component_plugin(self):
        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=MyButtonPlugin.__name__,
            language=self.language,
        )
        instance.initialize_from_form(MyButtonPlugin.form)
        instance.config["link"] = {"internal_link": f"cms.page:{self.page.pk}"}
        instance.save()

        from djangocms_link.templatetags.djangocms_link_tags import to_url

        link = to_url(instance.link)

        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'<a class="btn" href="{link}">Click me</a>', response.content.decode("utf-8"))

    def test_strange_plugin(self):
        self.assertEqual(MyStrangeComponentPlugin.name, "MyStrangeComponent")
        self.assertEqual(MyStrangeComponentPlugin.render_template, "djangocms_frontend/html_container.html")
        self.assertFalse(MyStrangeComponentPlugin.allow_children)

    def test_component_with_custom_fieldsets(self):
        """Test that components respect fieldsets provided in the Meta class"""
        # Check that the plugin uses custom fieldsets
        self.assertEqual(MyCardWithFieldsetsPlugin.name, "Card with Fieldsets")

        # Verify fieldsets are correctly set on the plugin
        fieldsets = MyCardWithFieldsetsPlugin.fieldsets

        # Should have 3 fieldsets
        self.assertEqual(len(fieldsets), 3)

        # First fieldset (None) should contain title and subtitle
        self.assertIsNone(fieldsets[0][0])
        self.assertIn("title", fieldsets[0][1]["fields"])
        self.assertIn("subtitle", fieldsets[0][1]["fields"])

        # Second fieldset ("Content") should contain body_text
        self.assertEqual(fieldsets[1][0], "Content")
        self.assertIn("body_text", fieldsets[1][1]["fields"])
        self.assertIn("collapse", fieldsets[1][1]["classes"])

        # Third fieldset ("Styling") should contain styling fields
        self.assertEqual(fieldsets[2][0], "Styling")
        self.assertIn("background_color", fieldsets[2][1]["fields"])
        self.assertIn("text_color", fieldsets[2][1]["fields"])
        self.assertIn("collapse", fieldsets[2][1]["classes"])
        self.assertEqual(fieldsets[2][1]["description"], "Customize the appearance of the card")

        # Test rendering with custom fieldsets
        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=MyCardWithFieldsetsPlugin.__name__,
            language=self.language,
        )
        instance.initialize_from_form(MyCardWithFieldsetsPlugin.form).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card Title", response.content.decode("utf-8"))
        self.assertIn("Card body text", response.content.decode("utf-8"))
