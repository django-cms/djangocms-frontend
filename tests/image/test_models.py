from django.test import TestCase

from djangocms_frontend.contrib.image.forms import ImageForm
from djangocms_frontend.contrib.image.models import Image

from ..helpers import get_filer_image


class PictureModelTestCase(TestCase):
    def test_instance(self):
        instance = Image.objects.create().initialize_from_form(ImageForm)
        self.assertEqual(str(instance), "Image (1)")
        self.assertEqual(instance.get_short_description(), "<file is missing>")

    def test_legacy_filer_reference_uses_backend_asset(self):
        image = get_filer_image()
        self.addCleanup(image.delete)
        instance = Image.objects.create(
            config={"picture": {"model": "filer.Image", "pk": image.pk}},
        )

        self.assertEqual(instance.picture_reference.backend, "filer")
        self.assertEqual(instance.picture_reference.id, str(image.pk))
        self.assertEqual(instance.image_asset.info.label, "test_file.jpg")
        self.assertEqual(instance.rel_image, image)

    def test_versioned_url_reference_uses_url_backend(self):
        instance = Image.objects.create(
            config={
                "picture": {
                    "version": 1,
                    "backend": "url",
                    "id": "https://example.com/image.jpg",
                    "context": {},
                    "snapshot": {"alt_text": "Example"},
                }
            },
        )

        self.assertEqual(instance.external_picture, "https://example.com/image.jpg")
        self.assertEqual(instance.img_src, "https://example.com/image.jpg")
        self.assertEqual(instance.image_alt_text, "Example")
