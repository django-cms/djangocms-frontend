from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.utilities.cms_plugins import (
    HeadingPlugin,
    SpacingPlugin,
    TOCPlugin,
)
from djangocms_frontend.contrib.utilities.forms import TableOfContentsForm

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
        self.assertContains(response, '<h2 id="id1" >Welcome to django CMS!</h2>')
        self.assertContains(
            response, '<h3 id="id2" >How you can benefit from django CMS</h3>'
        )
        self.assertContains(response, '<ul class="test-class"><li ><a href="#id2" >')
        self.assertContains(response, '<a href="#id1" >')
        self.assertContains(response, '<a href="#id2" >')
