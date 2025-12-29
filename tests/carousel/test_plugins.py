from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.test import override_settings

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

        # Now testing if links are working
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
            config=dict(
                carousel_image=dict(pk=self.image.id, model="filer.Image"),
                link=dict(external_link="https://www.divio.com"),
            ),
        )
        plugin.initialize_from_form(CarouselSlideForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="https://www.divio.com"')

    @override_settings(
        DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES=(
            ("default", "Default"),
            ("custom", "Custom"),
        )
    )
    def test_carousel_slide_inherits_parent_template(self):
        """Test that CarouselSlidePlugin correctly retrieves parent's template."""
        # Create a carousel with a custom template
        carousel = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
            config=dict(template="custom"),
        )
        carousel.initialize_from_form(CarouselForm).save()

        # Create a slide as child of the carousel
        slide = add_plugin(
            target=carousel,
            placeholder=self.placeholder,
            plugin_type=CarouselSlidePlugin.__name__,
            language=self.language,
            config=dict(carousel_image=dict(pk=self.image.id, model="filer.Image")),
        )
        slide.initialize_from_form(CarouselSlideForm).save()

        # Get the plugin instance
        plugin_instance = CarouselSlidePlugin()

        # Test that get_render_template uses the parent's template
        template_path = plugin_instance.get_render_template(context={}, instance=slide, placeholder=self.placeholder)

        # The template path should use 'custom' from the parent, not 'default'
        self.assertIn("custom", template_path)
        self.assertEqual(template_path, "djangocms_frontend/bootstrap5/carousel/custom/slide.html")
