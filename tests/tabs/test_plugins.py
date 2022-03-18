from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

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
