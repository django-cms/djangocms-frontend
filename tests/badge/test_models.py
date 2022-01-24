from django.test import TestCase

from djangocms_frontend.contrib.badge.forms import BadgeForm
from djangocms_frontend.contrib.badge.models import Badge


class BadgeModelTestCase(TestCase):
    def test_instance(self):
        instance = Badge.objects.create().initialize_from_form(BadgeForm)
        self.assertEqual(str(instance), "Badge (1)")
        self.assertEqual(instance.get_short_description(), "(primary)")
