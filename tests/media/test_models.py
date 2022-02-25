from django.test import TestCase

from djangocms_frontend.contrib.media.models import Media, MediaBody


class MediaModelTestCase(TestCase):
    def test_media_instance(self):
        instance = Media.objects.create()
        self.assertEqual(str(instance), "Media (1)")
        self.assertEqual(instance.get_short_description(), "")

    def test_media_body_instance(self):
        instance = MediaBody.objects.create()
        self.assertEqual(str(instance), "MediaBody (1)")
        self.assertEqual(instance.get_short_description(), "")
