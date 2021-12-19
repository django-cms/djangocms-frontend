from django.test import TestCase

from djangocms_frontend.contrib.picture.models import (
    Bootstrap5Picture,
)


class B5PictureModelTestCase(TestCase):

    def test_instance(self):
        instance = Bootstrap5Picture.objects.create()
        self.assertEqual(str(instance), "1")
