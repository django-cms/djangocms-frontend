from django.test import TestCase

from djangocms_frontend.contrib.link.models import Link


class LinkModelTestCase(TestCase):

    def test_instance(self):
        instance = Link.objects.create()
        self.assertEqual(str(instance), "Link (1)")
