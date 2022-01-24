from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin

from ..fixtures import TestFixture


class LinkPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
            ),
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="https://www.divio.com"')

        # add more options
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
                link_context="primary",
                link_size="btn-sm",
                link_block=True,
            ),
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text-primary")
        self.assertContains(response, "btn-sm")
        self.assertContains(response, "btn-block")

        # alternate version for link_type
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
                link_context="primary",
                link_type="btn",
            ),
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-primary")

        # alternate version using link_outline
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
                link_context="primary",
                link_type="btn",
                link_outline=True,
            ),
        )

        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('class="btn btn-outline-primary"' in response.content.decode("utf-8"))
            or ('class="btn-outline-primary btn"' in response.content.decode("utf-8")),
            f'Cound not find class="btn btn-outline-primary" in {response.content.decode("utf-8")}',
        )
