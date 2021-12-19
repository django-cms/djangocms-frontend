from django.test import TestCase

from djangocms_frontend.contrib.link.models import Bootstrap5Link


class B5LinkModelTestCase(TestCase):

    def test_instance(self):
        instance = Bootstrap5Link.objects.create()
        self.assertEqual(str(instance), "1")
