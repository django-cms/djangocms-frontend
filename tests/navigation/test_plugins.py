from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.navigation.cms_plugins import (
    NavContainerPlugin,
    NavigationPlugin,
    NavLinkPlugin,
    PageTreePlugin,
)
from djangocms_frontend.contrib.navigation.forms import (
    NavContainerForm,
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
            '<nav class="navbar-expand-xl navbar navbar-light">'
            in response.content.decode("utf-8")
            or '<nav class="navbar-expand-xl navbar-light navbar">'
            in response.content.decode("utf-8")
            or '<nav class="navbar navbar-light navbar-expand-xl">'
            in response.content.decode("utf-8")
            or '<nav class="navbar navbar-expand-xl navbar-light">'
            in response.content.decode("utf-8")
            or '<nav class="navbar-light navbar navbar-expand-xl">'
            in response.content.decode("utf-8")
            or '<nav class="navbar-light navbar-expand-xl navbar">'
            in response.content.decode("utf-8")
        )
        self.assertContains(response, '<div class="container"></div>')

        # add more options
        container = add_plugin(
            placeholder=self.placeholder,
            plugin_type=NavContainerPlugin.__name__,
            target=nav,
            language=self.language,
            config=dict(),
        )
        container.initialize_from_form(NavContainerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<ul class="navbar-nav"></ul>')
        self.assertContains(response, '<button class="navbar-toggler"')
        self.assertContains(response, 'id="nav')

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=NavLinkPlugin.__name__,
            language=self.language,
            target=container,
            config=dict(
                internal_link=dict(model="cms.page", pk=self.page.id),
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
            target=container,
            config=dict(),
        )
        plugin.initialize_from_form(PageTreeForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
