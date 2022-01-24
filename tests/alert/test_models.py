from django.test import TestCase

from djangocms_frontend.contrib.alert.forms import AlertForm
from djangocms_frontend.contrib.alert.models import Alert


class AlertModelTestCase(TestCase):
    def test_instance(self):
        instance = Alert.objects.create()
        instance.initialize_from_form(AlertForm).save()
        self.assertEqual(str(instance), "Alert (1)")
        self.assertEqual(instance.get_short_description(), "(primary)")
