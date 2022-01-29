from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.utilities.cms_plugins import SpacingPlugin

from ..fixtures import TestFixture


class UtilitiesPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=SpacingPlugin.__name__,
            language=self.language,
            config={
                "space_property": "m",
                "space_size": 0,
                "space_device": "xs",
                "space_sides": "",
            },
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="m-0">')
