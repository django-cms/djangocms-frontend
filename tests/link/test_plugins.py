from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse
from django.http import HttpRequest

from djangocms_frontend import settings
from djangocms_frontend.contrib.link.cms_plugins import TextLinkPlugin
from djangocms_frontend.contrib.link.forms import LinkForm, SmartLinkField
from djangocms_frontend.contrib.link.helpers import get_choices

from ..fixtures import TestFixture


class LinkPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextLinkPlugin.__name__,
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
            plugin_type=TextLinkPlugin.__name__,
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
            plugin_type=TextLinkPlugin.__name__,
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
        # Finally, test the descriptor
        self.assertEqual(plugin.internal_link, self.page)

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
                    else dict(external_link="https://www.django-cms.org/")
                ),
            }
        )
        form = LinkForm(request.POST)
        self.assertTrue(form.is_valid(), f"{form.__class__.__name__}:form errors: {form.errors}")
        if hasattr(self, "create_url"):
            self.delete_urls()
        else:
            request.POST.update({"mailto": "none@nowhere.com"})
            form = LinkForm(request.POST)
            self.assertFalse(form.is_valid())  # Two targets
            request.POST["external_link"] = None
            form = LinkForm(request.POST)
            self.assertFalse(form.is_valid())  # no anchor for mail


class AutocompleteViewTestCase(TestFixture, CMSTestCase):

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

    def test_autocomplete_view(self):
        tricky_title = """d'acceuil: <script>alert("XSS");</script>"""
        page = self.create_page(
            title=tricky_title,
            template="page.html",
        )
        expected_choices = [
            "home", "content", tricky_title,
        ]

        self.publish(page, self.language)
        autocomplete_url = admin_reverse("link_link_autocomplete")

        with self.login_user_context(self.superuser):
            response = self.client.get(autocomplete_url)

        autocomplete_result = response.json()
        choices = autocomplete_result.get("results")[0]

        self.assertFalse((autocomplete_result.get("pagination") or {}).get("more"))

        for expected, sent in zip(expected_choices, choices.get("children")):
            self.assertEqual(expected, sent.get("text"))
