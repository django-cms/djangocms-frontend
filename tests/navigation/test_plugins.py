from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.navigation.cms_plugins import (
    NavigationPlugin,
    NavLinkPlugin,
    PageTreePlugin,
)
from djangocms_frontend.contrib.navigation.forms import (
    NavigationForm,
    NavLinkForm,
    PageTreeForm,
)

from ..fixtures import TestFixture


class NavigationPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        nav = add_plugin(
            placeholder=self.placeholder,
            plugin_type=NavigationPlugin.__name__,
            language=self.language,
            config=dict(
                navbar_breakpoint="xl",
                navbar_container=True,
            ),
        ).initialize_from_form(NavigationForm)
        nav.save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '<nav class="navbar-expand-xl navbar navbar-light">' in response.content.decode("utf-8")
            or '<nav class="navbar-expand-xl navbar-light navbar">' in response.content.decode("utf-8")
            or '<nav class="navbar navbar-light navbar-expand-xl">' in response.content.decode("utf-8")
            or '<nav class="navbar navbar-expand-xl navbar-light">' in response.content.decode("utf-8")
            or '<nav class="navbar-light navbar navbar-expand-xl">' in response.content.decode("utf-8")
            or '<nav class="navbar-light navbar-expand-xl navbar">' in response.content.decode("utf-8")
        )
        self.assertContains(response, '<div class="container">')
        self.assertContains(response, '<span class="navbar-toggler-icon"></span>')
        self.assertContains(response, '<div class="collapse navbar-collapse"')
        self.assertContains(response, '<ul class="navbar-nav">')

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=NavLinkPlugin.__name__,
            language=self.language,
            target=nav,
            config=dict(
                link=dict(internal_link=f"cms.page:{self.page.id}"),
                link_context="primary",
                link_type="btn",
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(NavLinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-primary")
        self.assertContains(response, "nav-link")
        self.assertContains(response, 'href="/content/"')

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=PageTreePlugin.__name__,
            language=self.language,
            target=nav,
            config=dict(),
        )
        plugin.initialize_from_form(PageTreeForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
