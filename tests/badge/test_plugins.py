from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.badge.cms_plugins import BadgePlugin
from djangocms_frontend.contrib.badge.forms import BadgeForm

from ..fixtures import TestFixture


class BadgePluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=BadgePlugin.__name__,
            language=self.language,
            config=dict(
                badge_text="some text",
            ),
        )
        plugin.initialize_from_form(BadgeForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (
                '<span class="badge bg-primary">some text</span>'
                in response.content.decode("utf-8")
            )
            or (
                '<span class="bg-primary badge">some text</span>'
                in response.content.decode("utf-8")
            ),
            f'<span class="badge bg-primary">some text</span> not found in {response.content.decode("utf-8")}',
        )

        # test with pills enabled
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=BadgePlugin.__name__,
            language=self.language,
            config=dict(
                badge_text="some text",
                badge_pills=True,
            ),
        )
        plugin.initialize_from_form(BadgeForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rounded-pill")
        self.assertContains(response, "bg-primary")
        self.assertContains(response, "some text")
