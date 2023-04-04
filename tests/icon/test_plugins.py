from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.icon.cms_plugins import IconPlugin

from ..fixtures import TestFixture
from .test_models import icon_config


class IconPluginTestCase(TestFixture, CMSTestCase):
    def test_icon_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=IconPlugin.__name__,
            language=self.language,
            config=icon_config,
            tag_type="i",
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<i ')
        self.assertContains(response, 'zi-airplane')
        self.assertContains(response, '</i>')
        self.assertContains(response, 'style=')
        self.assertContains(response, '400%')
