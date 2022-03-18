from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.jumbotron.cms_plugins import JumbotronPlugin

from ..fixtures import TestFixture


class JumbotronPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=JumbotronPlugin.__name__,
            language=self.language,
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "container")

        # fluid option
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=JumbotronPlugin.__name__,
            language=self.language,
            config=dict(
                jumbotron_fluid=True,
            ),
        )
        plugin.full_clean()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "container-fluid")
