from unittest import skipIf

from cms import __version__ as cms_version
from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse
from djangocms_text.cms_plugins import TextPlugin

from djangocms_frontend.contrib.utilities.cms_plugins import (
    EditorNotePlugin,
    HeadingPlugin,
    SpacingPlugin,
    TOCPlugin,
)
from djangocms_frontend.contrib.utilities.forms import TableOfContentsForm
from djangocms_frontend.ui_plugin_base import PlaceholderAdmin

from ..fixtures import TestFixture


class UtilitiesPluginTestCase(TestFixture, CMSTestCase):
    def test_spacing(self):
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
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="m-0">')

    def test_heading(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TOCPlugin.__name__,
            language=self.language,
            config=dict(list_attributes={"class": "empty-toc"}),
        ).initialize_from_form(TableOfContentsForm).save()
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=HeadingPlugin.__name__,
            language=self.language,
            config={
                "heading_level": "h2",
                "heading": "Welcome to django CMS!",
                "heading_id": "id1",
            },
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=HeadingPlugin.__name__,
            language=self.language,
            config={
                "heading_level": "h3",
                "heading": "How you can benefit from django CMS",
                "heading_id": "id2",
            },
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=HeadingPlugin.__name__,
            language=self.language,
            config={
                "heading_level": "h2",
                "heading": "Great, isn't it?",
                "heading_id": "id3",
            },
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TOCPlugin.__name__,
            language=self.language,
            config=dict(list_attributes={"class": "test-class"}),
        ).initialize_from_form(TableOfContentsForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<ul class="empty-toc"></ul>')
        self.assertContains(response, '<h2 id="id1">Welcome to django CMS!</h2>')
        self.assertContains(response, '<h3 id="id2">How you can benefit from django CMS</h3>')
        self.assertContains(response, '<ul class="test-class"><li ><a href="#id2" >')
        self.assertContains(response, '<a href="#id1" >')
        self.assertContains(response, '<a href="#id2" >')

    def test_heading_inline_endpoint(self):
        heading = add_plugin(
            placeholder=self.placeholder,
            plugin_type=HeadingPlugin.__name__,
            language=self.language,
            config={
                "heading_level": "h2",
                "heading": "Welcome to django CMS!",
                "heading_id": "id1",
            },
        )

        if hasattr(PlaceholderAdmin, "edit_field"):
            url_endpoint = "cms_placeholder_edit_field"
        else:
            url_endpoint = "utilities_heading_edit_field"
        url_endpoint = admin_reverse(url_endpoint, args=[heading.pk, self.language]) + "?edit_fields=heading"
        data = {
            "heading": "My new heading",
        }
        with self.login_user_context(self.superuser):
            response = self.client.post(url_endpoint, data)

        self.assertEqual(response.status_code, 200)
        heading.refresh_from_db()
        self.assertEqual(heading.heading, "My new heading")  # New data
        self.assertEqual(heading.heading_id, "id1")  # Other fields unchanged

    def test_editor_note(self):
        editor_note = add_plugin(
            placeholder=self.placeholder,
            plugin_type=EditorNotePlugin.__name__,
            language=self.language,
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextPlugin.__name__,
            language=self.language,
            target=editor_note,
            body="<p>My private note</p>",
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "My private note")

    @skipIf(cms_version < "4", "django CMS 4+ required")
    def test_editor_note_with_cms4(self):
        from cms.toolbar.utils import get_object_edit_url

        editor_note = add_plugin(
            placeholder=self.placeholder,
            plugin_type=EditorNotePlugin.__name__,
            language=self.language,
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=TextPlugin.__name__,
            language=self.language,
            target=editor_note,
            body="<p>My private note</p>",
        )

        endpoint = get_object_edit_url(self.page.get_admin_content("en"))

        with self.login_user_context(self.superuser):
            response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My private note")
