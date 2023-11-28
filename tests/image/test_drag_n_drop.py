from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.image.models import Image
from tests.fixtures import TestFixture


class DjangoCMSPictureIntegrationTestCase(TestFixture, CMSTestCase):
    def setUp(self):
        super().setUp()
        self.placeholder = self.get_placeholders(self.home).get(slot='content')

    def test_extract_images(self):
        text_plugin = add_plugin(
            self.placeholder,
            'TextPlugin',
            'en',
            body='<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42m'
                 'P8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==">',
        )

        picture_plugins = Image.objects.order_by('-id')
        self.assertEqual(len(picture_plugins), 1)
        self.assertEqual(picture_plugins[0].parent.id, text_plugin.id)
        id = picture_plugins[0].id
        self.assertHTMLEqual(
            text_plugin.body,
            f'<cms-plugin alt="Picture / Image - Image ({id}) " '
            f'title="Picture / Image - Image ({id})" '
            f'id="{id}"></cms-plugin>',
        )
