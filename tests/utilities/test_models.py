from django.test import TestCase

from djangocms_frontend.contrib.utilities.models import (
    Spacing,
)


class B5UtilitiesModelTestCase(TestCase):

    def test_instance(self):
        instance = Spacing.objects.create(config={
            "space_device": "",
            "space_property": "m",
            "space_size": 0,
            "space_sides": "",
        })
        self.assertEqual(str(instance), "Spacing (1)")
        self.assertEqual(instance.get_short_description(), "(.m-0)")

        instance.config["space_device"] = "md"
        self.assertEqual(instance.get_short_description(), "(.m-md-0)")
