from django.test import TestCase

from djangocms_frontend.contrib.jumbotron.models import Jumbotron


class JumbotronModelTestCase(TestCase):
    def test_instance(self):
        instance = Jumbotron.objects.create()
        instance.config["jumbotron_fluid"] = False
        self.assertEqual(str(instance), "Jumbotron (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.config["jumbotron_fluid"] = True
        self.assertEqual(instance.get_short_description(), "(Fluid)")
