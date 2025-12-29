from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.test import override_settings

from djangocms_frontend.contrib.tabs.cms_plugins import TabItemPlugin, TabPlugin
from djangocms_frontend.contrib.tabs.forms import TabForm, TabItemForm

from ..fixtures import TestFixture


class TabsPluginTestCase(TestFixture, CMSTestCase):
    def test_tab_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TabPlugin.__name__,
            language=self.language,
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nav")

    def test_tab_item_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TabPlugin.__name__,
            language=self.language,
        ).initialize_from_form(TabForm)
        parent.save()
        add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=TabItemPlugin.__name__,
            language=self.language,
            config=dict(tab_title="tab title"),
        ).initialize_from_form(TabItemForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="tab-content">')
        self.assertContains(response, "tab-pane")

    @override_settings(
        DJANGOCMS_FRONTEND_TAB_TEMPLATES=(
            ("default", "Default"),
            ("custom", "Custom"),
        )
    )
    def test_tab_item_inherits_parent_template(self):
        """Test that TabItemPlugin correctly retrieves parent's template."""
        # Create a tab container with a custom template
        tab_container = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TabPlugin.__name__,
            language=self.language,
            config=dict(template="custom"),
        )
        tab_container.initialize_from_form(TabForm).save()

        # Create a tab item as child of the tab container
        tab_item = add_plugin(
            target=tab_container,
            placeholder=self.placeholder,
            plugin_type=TabItemPlugin.__name__,
            language=self.language,
            config=dict(tab_title="Test Tab"),
        )
        tab_item.initialize_from_form(TabItemForm).save()

        # Get the plugin instance
        plugin_instance = TabItemPlugin()

        # Test that get_render_template uses the parent's template
        template_path = plugin_instance.get_render_template(
            context={}, instance=tab_item, placeholder=self.placeholder
        )

        # The template path should use 'custom' from the parent, not 'default'
        self.assertIn("custom", template_path)
        self.assertEqual(template_path, "djangocms_frontend/bootstrap5/tabs/custom/item.html")
