from django.test import TestCase

from djangocms_frontend.contrib.image.models import Image


class PictureModelTestCase(TestCase):
    def test_instance(self):
        instance = Image.objects.create()
        self.assertEqual(str(instance), "Image (1)")
