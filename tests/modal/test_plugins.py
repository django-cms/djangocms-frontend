from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.modal.cms_plugins import (
    ModalContainerPlugin,
    ModalPlugin,
    ModalTriggerPlugin,
    ModalModalInnerPlugin
)
from djangocms_frontend.contrib.modal.forms import (
    ModalContainerForm,
    ModalForm,
    ModalTriggerForm,
    ModalModalInnerForm
)

from ..fixtures import TestFixture


class ModalPluginTestCase(TestFixture, CMSTestCase):
    def test_modal_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ModalPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(ModalForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-bs-children=".modal"')

    def test_modal_trigger_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ModalTriggerPlugin.__name__,
            language=self.language,
            config=dict(
                trigger_identifier=10,
            ),
        )
        plugin.initialize_from_form(ModalTriggerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-controls="10"')
        self.assertContains(response, 'data-bs-target="#10"')
        self.assertContains(response, 'id="trigger-10"')

    def test_modal_container_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ModalPlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(ModalForm).save()

        plugin = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=ModalContainerPlugin.__name__,
            language=self.language,
            config=dict(
                container_identifier=10,
            ),
        )
        plugin.initialize_from_form(ModalContainerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-labelledby="trigger-10"')
        self.assertContains(response, "10")
