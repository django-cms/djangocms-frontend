from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.collapse.cms_plugins import (
    CollapseContainerPlugin,
    CollapsePlugin,
    CollapseTriggerPlugin,
)
from djangocms_frontend.contrib.collapse.forms import (
    CollapseContainerForm,
    CollapseForm,
    CollapseTriggerForm,
)

from ..fixtures import TestFixture


class CollapsePluginTestCase(TestFixture, CMSTestCase):
    def test_collapse_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapsePlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CollapseForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-bs-children=".card"')
        self.assertContains(response, 'role="tablist"')

    def test_collapse_trigger_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapseTriggerPlugin.__name__,
            language=self.language,
            config=dict(
                trigger_identifier=10,
            ),
        )
        plugin.initialize_from_form(CollapseTriggerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-controls="10"')
        self.assertContains(response, 'data-bs-target="#10"')
        self.assertContains(response, 'id="trigger-10"')

    def test_collapse_container_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapsePlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(CollapseForm).save()

        plugin = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=CollapseContainerPlugin.__name__,
            language=self.language,
            config=dict(
                container_identifier=10,
            ),
        )
        plugin.initialize_from_form(CollapseContainerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-labelledby="trigger-10"')
        self.assertContains(response, "10")
