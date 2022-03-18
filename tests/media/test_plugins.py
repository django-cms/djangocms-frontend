from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.media.cms_plugins import MediaBodyPlugin, MediaPlugin

from ..fixtures import TestFixture


class MediaPluginTestCase(TestFixture, CMSTestCase):
    def test_media_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=MediaPlugin.__name__,
            language=self.language,
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="flex-shrink-0">')

    def test_media_body_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=MediaBodyPlugin.__name__,
            language=self.language,
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "flex-grow-1")
