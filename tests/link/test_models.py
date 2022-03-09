from django.test import TestCase

from djangocms_frontend.contrib.link.models import Link


class LinkModelTestCase(TestCase):
    def test_instance(self):
        instance = Link.objects.create(
            config=dict(name="Get it!", external_link="https://www.django-cms.com/")
        )
        self.assertEqual(str(instance), "Link (1)")
        self.assertEqual(
            instance.get_short_description(), "Get it! (https://www.django-cms.com/)"
        )
