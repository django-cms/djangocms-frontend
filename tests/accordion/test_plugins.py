from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.accordion.cms_plugins import (
    AccordionItemPlugin,
    AccordionPlugin,
)
from djangocms_frontend.contrib.accordion.forms import AccordionForm, AccordionItemForm

from ..fixtures import TestFixture


class AccordionPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AccordionPlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(AccordionForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="parent-1"')

        plugin = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=AccordionItemPlugin.__name__,
            language=self.language,
            config=dict(attributes={"class": "test-class"}),
        )
        plugin.initialize_from_form(AccordionItemForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="accordion-item">')
        self.assertTrue(
            (
                'class="collapse accordion-collapse test-class"'
                in response.content.decode("utf-8")
            )
            or (
                'class="accordion-collapse collapse test-class"'
                in response.content.decode("utf-8")
            )
            or (
                'class="accordion-collapse test-class collapse"'
                in response.content.decode("utf-8")
            )
            or (
                'class="collapse test-class accordion-collapse"'
                in response.content.decode("utf-8")
            )
            or (
                'class="test-class collapse accordion-collapse"'
                in response.content.decode("utf-8")
            )
            or (
                'class="test-class accordion-collapse collapse"'
                in response.content.decode("utf-8")
            ),
            f'<div class="collapse accordion-collapse test-class"> not found in {response.content.decode("utf-8")}',
        )
        self.assertContains(response, 'id="heading-')
