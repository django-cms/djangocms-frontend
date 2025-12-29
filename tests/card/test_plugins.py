from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.card.cms_plugins import CardInnerPlugin, CardPlugin
from djangocms_frontend.contrib.card.forms import CardForm, CardInnerForm
from djangocms_frontend.contrib.image.cms_plugins import ImagePlugin
from djangocms_frontend.contrib.image.forms import ImageForm

from ..fixtures import TestFixture
from ..helpers import get_filer_image


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
            or ('<div class="bg-transparent card">' in response.content.decode("utf-8")),
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

    def test_card_image(self):
        self.image = get_filer_image()

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CardForm).save()
        image = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ImagePlugin.__name__,
            language=self.language,
            target=plugin,
            config={
                "picture": {"pk": self.image.id, "model": "filer.Image"},
                "use_responsive_image": "yes",
            },
        )
        image.initialize_from_form(ImageForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "card-img-top")
        self.assertNotContains(response, "card-img-bottom")

        # add inner type above image
        inner = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CardInnerPlugin.__name__,
            language=self.language,
            target=plugin,
            position="first-child",  # before image
            config=dict(
                inner_type="card-header",
            ),
        )
        inner.initialize_from_form(CardInnerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "card-img-top")
        self.assertContains(response, "card-img-bottom")

        self.image.delete()
