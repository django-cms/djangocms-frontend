from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm

from ..fixtures import TestFixture


class AlertPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(AlertForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (
                '<div class="alert alert-primary" role="alert">'
                in response.content.decode("utf-8")
            )
            or (
                '<div class="alert-primary alert" role="alert">'
                in response.content.decode("utf-8")
            ),
            f'alert-primary not found in {response.content.decode("utf-8")}',
        )
