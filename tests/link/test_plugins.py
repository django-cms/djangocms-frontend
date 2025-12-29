from unittest.mock import Mock

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.http import HttpRequest
from django.test import RequestFactory

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
                    dict(url_grouper=str(self.create_url(manual_url="https://www.django-cms.org/").id))
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

    def test_link_form_add_view_name_not_required_by_default(self):
        """Test that name is not required in add view when not child of TextPlugin"""
        plugin = TextLinkPlugin()
        request = RequestFactory().get("/")
        request.user = self.superuser

        # No parent set, so name_required should be False
        plugin._cms_initial_attributes = {}
        form_class = plugin.get_form(request, obj=None, change=False)

        # Instantiate form to check field requirement
        form = form_class()
        # name_required should be False when no parent
        self.assertFalse(getattr(form, "name_required", False))
        self.assertFalse(form.fields["name"].required)

    def test_link_form_add_view_name_required_for_text_plugin_child(self):
        """Test that name is required in add view when child of TextPlugin"""
        plugin = TextLinkPlugin()
        request = RequestFactory().get("/")
        request.user = self.superuser

        # Mock a TextPlugin parent
        parent = Mock()
        parent.plugin_type = "TextPlugin"
        plugin._cms_initial_attributes = {"parent": parent}

        # Get form for add view with TextPlugin parent
        form_class = plugin.get_form(request, obj=None, change=False)

        # Instantiate form to check field requirement
        form = form_class()
        # name_required should be True when parent is TextPlugin
        self.assertTrue(getattr(form, "name_required", False))
        # Verify the field requirement is set correctly
        self.assertTrue(form.fields["name"].required)

    def test_link_form_change_view_name_required_for_text_plugin_child(self):
        """Test that form validation fails when name is required for TextPlugin child"""
        request = HttpRequest()
        request.POST = {
            "template": settings.LINK_TEMPLATE_CHOICES[0][0],
            "link_type": "link",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **(
                dict(url_grouper=str(self.create_url(manual_url="https://www.django-cms.org/").id))
                if hasattr(self, "create_url")
                else dict(
                    link_0="external_link",
                    link_1="https://www.django-cms.org/",
                )
            ),
            # name field is empty
        }
        form = LinkForm(request.POST)
        form.name_required = True  # Simulate child of TextPlugin
        # Update field requirement as get_form() would do
        form.fields["name"].required = form.name_required
        # Form should be invalid without name when child of TextPlugin
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        if hasattr(self, "create_url"):
            self.delete_urls()

    def test_link_form_change_view_name_not_required_without_text_plugin_parent(self):
        """Test that form validation passes when name is not required"""
        request = HttpRequest()
        request.POST = {
            "template": settings.LINK_TEMPLATE_CHOICES[0][0],
            "link_type": "link",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **(
                dict(url_grouper=str(self.create_url(manual_url="https://www.django-cms.org/").id))
                if hasattr(self, "create_url")
                else dict(
                    link_0="external_link",
                    link_1="https://www.django-cms.org/",
                )
            ),
            # name field is empty
        }
        form = LinkForm(request.POST)
        form.name_required = False  # Not a child of TextPlugin
        # Form should be valid without name when not child of TextPlugin
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        if hasattr(self, "create_url"):
            self.delete_urls()
