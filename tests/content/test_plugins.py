from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.content.cms_plugins import (
    BlockquotePlugin,
    CodePlugin,
    FigurePlugin,
)
from djangocms_frontend.contrib.content.forms import BlockquoteForm, FigureForm

from ..fixtures import TestFixture


class ContentPluginTestCase(TestFixture, CMSTestCase):
    def test_code_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=CodePlugin.__name__,
            language=self.language,
            config=dict(
                code_content="<p>hello world</p>",
            ),
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;p&gt;hello world&lt;/p&gt;")

    def test_blockquote_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=BlockquotePlugin.__name__,
            language=self.language,
            config=dict(
                quote_content="hello world",
            ),
        )
        plugin.initialize_from_form(BlockquoteForm)
        plugin.save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<blockquote class="blockquote">')

        # test quote_alignment
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=BlockquotePlugin.__name__,
            language=self.language,
            config=dict(
                quote_content="hello world",
                quote_alignment="",
            ),
        )
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<blockquote class="blockquote">')

    def test_figure_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=FigurePlugin.__name__,
            language=self.language,
            config=dict(
                figure_caption="hello world",
            ),
        )
        plugin.initialize_from_form(FigureForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<figcaption class="figure-caption')
