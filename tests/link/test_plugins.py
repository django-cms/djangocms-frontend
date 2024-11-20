from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.http import HttpRequest

from djangocms_frontend import settings
from djangocms_frontend.contrib.link.cms_plugins import TextLinkPlugin
from djangocms_frontend.contrib.link.forms import LinkForm

from ..fixtures import TestFixture


class LinkPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
            language=self.language,
            config=dict(
                link=dict(external_link="https://www.divio.com"),
            ),
        ).initialize_from_form(LinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="https://www.divio.com"')

        # add more options
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
            language=self.language,
            config=dict(
                dict(link=dict(external_link="https://www.divio.com")),
                link_context="primary",
                link_size="btn-sm",
                link_block=True,
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "link-primary")
        self.assertContains(response, "btn-sm")
        self.assertContains(response, "d-block")

        # alternate version for link_type
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
            language=self.language,
            config=dict(
                link=dict(internal_link=f"cms.page:{self.page.id}"),
                link_context="primary",
                link_type="btn",
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-primary")
        self.assertContains(response, 'href="/content/"')

        # alternate version broken link
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
            language=self.language,
            config=dict(
                internal_link=dict(model="cms.page", pk=-3141),
                link_context="primary",
                link_type="btn",
                link_outline=True,
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\ndjango CMS rocks")

        # alternate version using link_outline
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
            language=self.language,
            config=dict(
                link=dict(external_link="https://www.divio.com"),
                link_context="primary",
                link_type="btn",
                link_outline=True,
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('class="btn btn-outline-primary"' in response.content.decode("utf-8"))
            or ('class="btn-outline-primary btn"' in response.content.decode("utf-8")),
            f'Cound not find class="btn btn-outline-primary" in {response.content.decode("utf-8")}',
        )

    def test_link_form(self):
        request = HttpRequest()
        request.POST = {
            "template": settings.LINK_TEMPLATE_CHOICES[0][0],
            "link_type": "link",
        }
        form = LinkForm(request.POST)
        self.assertFalse(form.is_valid())
        request.POST.update(
            {
                "name": "One of the world's most advanced open source CMS",
                "anchor": "allowed-here",
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
                **(
                    dict(
                        url_grouper=str(
                            self.create_url(manual_url="https://www.django-cms.org/").id
                        )
                    )
                    if hasattr(self, "create_url")
                    else dict(
                        link_0="external_link",
                        link_1="https://www.django-cms.org/",
                    )
                ),
            }
        )
        form = LinkForm(request.POST)
        self.assertTrue(form.is_valid(), f"{form.__class__.__name__}:form errors: {form.errors}")
        if hasattr(self, "create_url"):
            self.delete_urls()
