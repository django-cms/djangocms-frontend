from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.http import HttpRequest

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin
from djangocms_frontend.contrib.link.forms import (
    LinkForm,
    SmartLinkField,
    get_templates,
)
from djangocms_frontend.contrib.link.helpers import get_choices

from ..fixtures import DJANGO_CMS4, TestFixture


class LinkPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
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
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
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
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                internal_link=dict(model="cms.page", pk=self.page.id),
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
            plugin_type=LinkPlugin.__name__,
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
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
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

    def test_smart_link_field(self):
        slf = SmartLinkField()
        choices = get_choices(None)
        self.assertEqual("example.com", choices[0][0])  # Site name
        self.assertIn(("2-1", "home"), choices[0][1])

        cleaned = slf.clean("2-1")
        self.assertEqual(dict(model="cms.page", pk=1), cleaned)

        self.assertEqual(slf.prepare_value("blabla"), "")
        self.assertEqual(slf.prepare_value(dict(model="cms.page", pk=1)), "2-1")
        self.assertEqual(slf.prepare_value(self.home), "2-1")

    def test_link_form(self):
        request = HttpRequest()
        request.POST = {
            "template": get_templates()[0][0],
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
                    if DJANGO_CMS4
                    else dict(external_link="https://www.django-cms.com/")
                ),
            }
        )
        form = LinkForm(request.POST)
        self.assertTrue(form.is_valid())
        if DJANGO_CMS4:
            self.delete_urls()
        else:
            request.POST.update({"mailto": "none@nowhere.com"})
            form = LinkForm(request.POST)
            self.assertFalse(form.is_valid())  # Two targets
            request.POST["external_link"] = None
            form = LinkForm(request.POST)
            self.assertFalse(form.is_valid())  # no anchor for mail
