from django.test import TestCase

from djangocms_frontend.contrib.carousel.forms import CarouselForm, CarouselSlideForm
from djangocms_frontend.contrib.carousel.models import Carousel, CarouselSlide

from ..helpers import get_filer_image


class CarouselModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.image = get_filer_image()

    def tearDown(self):
        super().tearDown()
        self.image.delete()

    def test_carousel_instance(self):
        instance = Carousel.objects.create()
        instance.initialize_from_form(CarouselForm).save()
        self.assertEqual(str(instance), "Carousel (1)")
        self.assertEqual(
            instance.get_short_description(),
            "(default) Interval: 5000, Controls: True, Indicators: True, "
            "Keyboard: True, Pause: hover, Ride: carouselWrap: True",
        )

    def test_carousel_slide_instance(self):
        instance = CarouselSlide.objects.create()
        instance.initialize_from_form(CarouselSlideForm).save()
        self.assertEqual(str(instance), "CarouselSlide (1)")
        self.assertEqual(instance.get_short_description(), "")
        # test carousel content strings
        instance.config["carousel_image"] = dict(pk=self.image.id, model="filer.Image")
        instance.config["carousel_content"] = "hello world"
        self.assertEqual(
            instance.get_short_description(),
            "test_file.jpg (hello world)",
        )
        instance.config["carousel_content"] = "hello world" + 100 * "#"
        self.assertEqual(
            instance.get_short_description(),
            "test_file.jpg (hello world" + "#" * 89 + "...)",
        )
        self.assertEqual(instance.get_link(), "")
        # # test image output options
        # instance.config["carousel_content"] = None
        # instance.config["carousel_image"] = dict(pk=get_filer_image(name="image").id, model="filer.Image")
        # self.assertEqual(instance.get_short_description(), "image")
        # instance.config["carousel_image"] = dict(
        #     pk=get_filer_image(name="image", original_filename=False).id, model="filer.Image"
        # )
        # self.assertEqual(instance.get_short_description(), "Image")
