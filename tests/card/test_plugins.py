from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.card.cms_plugins import CardInnerPlugin, CardPlugin
from djangocms_frontend.contrib.card.forms import CardForm, CardInnerForm

from ..fixtures import TestFixture


class CardPluginTestCase(TestFixture, CMSTestCase):
    def test_card_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CardForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card">')

        # add card type
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardPlugin.__name__,
            language=self.language,
            config=dict(
                card_outline="transparent",
                card_alignment="text-start",
                card_text_color="white",
            ),
        )
        plugin.initialize_from_form(CardForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "border-transparent")
        self.assertContains(response, "text-white")
        self.assertContains(response, "text-start")

        # special case when card outline is given but not card context
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardPlugin.__name__,
            language=self.language,
            config=dict(
                background_context="transparent",
            ),
        )
        plugin.initialize_from_form(CardForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('<div class="card bg-transparent">' in response.content.decode("utf-8"))
            or (
                '<div class="bg-transparent card">' in response.content.decode("utf-8")
            ),
            f'<div class="card bg-transparent"> not found in {response.content.decode("utf-8")}',
        )

    def test_card_inner_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardInnerPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CardInnerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card-body">')

        # add inner type
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardInnerPlugin.__name__,
            language=self.language,
            config=dict(
                inner_type="card-footer",
            ),
        )
        plugin.initialize_from_form(CardInnerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card-footer">')
