from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.listgroup.cms_plugins import (
    ListGroupItemPlugin,
    ListGroupPlugin,
)
from djangocms_frontend.contrib.listgroup.forms import ListGroupForm, ListGroupItemForm

from ..fixtures import TestFixture


class ListGroupPluginTestCase(TestFixture, CMSTestCase):
    def test_list_group_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=ListGroupPlugin.__name__,
            language=self.language,
            config=dict(list_group_flush=False),
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="list-group">')

        # test list_group_flush option
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ListGroupPlugin.__name__,
            language=self.language,
            config=dict(list_group_flush=True),
        )
        plugin.initialize_from_form(ListGroupForm)
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (
                '<div class="list-group list-group-flush">'
                in response.content.decode("utf-8")
            )
            or (
                '<div class="list-group-flush list-group">'
                in response.content.decode("utf-8")
            ),
            '<div class="list-group-flush list-group"> not in response',
        )

    def test_list_group_item_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ListGroupItemPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(ListGroupItemForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="list-group-item">')

        # test list_context and list_state options
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=ListGroupItemPlugin.__name__,
            language=self.language,
            config=dict(
                list_context="primary",
                list_state="active",
            ),
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "active")
        self.assertContains(response, "list-group-item-primary")
