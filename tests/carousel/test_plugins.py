from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.carousel.cms_plugins import (
    CarouselPlugin,
    CarouselSlidePlugin,
)
from djangocms_frontend.contrib.carousel.forms import CarouselForm, CarouselSlideForm

from ..fixtures import TestFixture
from ..helpers import get_filer_image


class CarouselPluginTestCase(TestFixture, CMSTestCase):
    def setUp(self):
        super().setUp()
        self.image = get_filer_image()

    def tearDown(self):
        super().tearDown()
        self.image.delete()

    def test_carousel_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CarouselForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('<div class="slide carousel"' in response.content.decode("utf-8"))
            or ('<div class="carousel slide"' in response.content.decode("utf-8")),
            f'<div class="slide carousel" not found in {response.content.decode("utf-8")}',
        )
        self.assertContains(response, 'data-bs-interval="5000"')
        self.assertContains(response, 'data-bs-keyboard="true"')
        self.assertContains(response, 'data-bs-pause="hover"')
        self.assertContains(response, 'data-bs-ride="carousel"')
        self.assertContains(response, 'data-bs-wrap="true"')

    def test_carousel_slide_plugin(self):
        row = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
        )
        row.initialize_from_form(CarouselForm).save()
        plugin = add_plugin(
            target=row,
            placeholder=self.placeholder,
            plugin_type=CarouselSlidePlugin.__name__,
            language=self.language,
            config=dict(carousel_image=dict(pk=self.image.id, model="filer.Image")),
        )
        plugin.initialize_from_form(CarouselSlideForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('<div class="slide carousel"' in response.content.decode("utf-8"))
            or ('<div class="carousel slide"' in response.content.decode("utf-8")),
            f'<div class="slide carousel" not found in {response.content.decode("utf-8")}',
        )

        # testing aspect ratio variant
        # also testing multiply entries
        row = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
            config=dict(
                carousel_aspect_ratio="16x9",
            ),
        )
        row.initialize_from_form(CarouselForm).save()
        add_plugin(
            target=row,
            placeholder=self.placeholder,
            plugin_type=CarouselSlidePlugin.__name__,
            language=self.language,
            config=dict(carousel_image=dict(pk=self.image.id, model="filer.Image")),
        ).initialize_from_form(CarouselSlideForm).save()
        add_plugin(
            target=row,
            placeholder=self.placeholder,
            plugin_type=CarouselSlidePlugin.__name__,
            language=self.language,
            config=dict(carousel_image=dict(pk=self.image.id, model="filer.Image")),
        ).initialize_from_form(CarouselSlideForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('<div class="slide carousel"' in response.content.decode("utf-8"))
            or ('<div class="carousel slide"' in response.content.decode("utf-8")),
            f'<div class="slide carousel" not found in {response.content.decode("utf-8")}',
        )
