from django.test import TestCase

from djangocms_frontend.contrib.alert.models import (
    Bootstrap5Alerts,
)


class B5AlertModelTestCase(TestCase):

    def test_instance(self):
        instance = Bootstrap5Alerts.objects.create()
        self.assertEqual(str(instance), "1")
        self.assertEqual(instance.get_short_description(), "(primary)")
