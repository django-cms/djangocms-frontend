from django.test import TestCase

from djangocms_frontend.contrib.utilities.models import (
    Heading,
    Spacing,
    TableOfContents,
)


class B5UtilitiesModelTestCase(TestCase):
    def test_instance(self):
        instance = Spacing.objects.create(
            config={
                "space_device": "",
                "space_property": "m",
                "space_size": 0,
                "space_sides": "",
            }
        )
        self.assertEqual(str(instance), "Spacing (1)")
        self.assertEqual(instance.get_short_description(), "(.m-0)")

        instance.config["space_device"] = "md"
        self.assertEqual(instance.get_short_description(), "(.m-md-0)")

        instance = Heading.objects.create(
            config=dict(
                heading_level="h2",
                heading="Welcome to Django-CMS!",
            )
        )
        self.assertEqual(str(instance), "Heading (2)")
        self.assertEqual(instance.get_short_description(), "(Welcome to Django-CMS!)")

        instance = TableOfContents.objects.create()
        self.assertEqual(str(instance), "TableOfContents (3)")
        self.assertEqual(instance.get_short_description(), "(3)")
