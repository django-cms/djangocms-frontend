from django.test import TestCase

from djangocms_frontend.contrib.image.forms import ImageForm
from djangocms_frontend.contrib.image.models import Image


class PictureModelTestCase(TestCase):
    def test_instance(self):
        instance = Image.objects.create().initialize_from_form(ImageForm)
        self.assertEqual(str(instance), "Image (1)")
        self.assertEqual(instance.get_short_description(), "<file is missing>")
