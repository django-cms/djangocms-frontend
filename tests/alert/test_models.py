from django.test import TestCase

from djangocms_frontend.contrib.alert.models import (
    Alert,
)


class AlertModelTestCase(TestCase):

    def test_instance(self):
        instance = Alert.objects.create()
        self.assertEqual(str(instance), "Alert (1)")
        self.assertEqual(instance.get_short_description(), "(primary)")
