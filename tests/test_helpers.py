from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.template.loader import select_template

from djangocms_frontend.contrib.carousel.cms_plugins import CarouselPlugin
from djangocms_frontend.contrib.carousel.constants import CAROUSEL_TEMPLATE_CHOICES
from djangocms_frontend.helpers import (
    first_choice,
    get_plugin_template,
    get_template_path,
    insert_fields,
    link_to_framework_doc,
)

from .fixtures import TestFixture


class HelpersTestCase(TestFixture, CMSTestCase):
    def test_get_template_path(self):
        template = get_template_path("carousel", "default", "slide")
        result = "djangocms_frontend/bootstrap5/carousel/default/slide.html"
        self.assertEqual(template, result)
        status = select_template([template])
        self.assertEqual(status.template.name, result)

    def test_get_plugin_template(self):
        self.superuser = self.get_superuser()
        self.language = "en"
        instance = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language="en",
        )
        template = get_plugin_template(
            instance,
            "carousel",
            "carousel",
            CAROUSEL_TEMPLATE_CHOICES,
        )
        self.assertEqual(
            template, "djangocms_frontend/bootstrap5/carousel/default/carousel.html"
        )
        # trigger default template
        template = get_plugin_template(
            instance,
            "does_not",
            "exist",
            CAROUSEL_TEMPLATE_CHOICES,
        )
        self.assertEqual(
            template, "djangocms_frontend/bootstrap5/does_not/default/exist.html"
        )
        # cleanup
        self.page.delete()

    def test_insert_fields(self):
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "F1",
                        "F2",
                        "F3",
                    )
                },
            ),
        )
        fs = insert_fields(fieldsets, ("F4",), block=0)
        self.assertEqual(
            fs,
            [
                (
                    None,
                    {
                        "fields": [
                            "F1",
                            "F2",
                            "F3",
                            "F4",
                        ],
                    },
                ),
            ],
        )
        fs = insert_fields(fieldsets, ("F4",), position=1, block=0)
        self.assertEqual(
            fs,
            [
                (
                    None,
                    {
                        "fields": [
                            "F1",
                            "F4",
                            "F2",
                            "F3",
                        ],
                    },
                ),
            ],
        )
        fs = insert_fields(fieldsets, ("F4",), position=-2, block=0)
        self.assertEqual(
            fs,
            [
                (
                    None,
                    {
                        "fields": [
                            "F1",
                            "F2",
                            "F4",
                            "F3",
                        ],
                    },
                ),
            ],
        )

        fs = insert_fields(fieldsets, ("F4",), blockname="Tarantula")
        self.assertEqual(
            fs,
            [
                (
                    None,
                    {
                        "fields": (
                            "F1",
                            "F2",
                            "F3",
                        ),
                    },
                ),
                (
                    "Tarantula",
                    {
                        "classes": ("collapse",),
                        "fields": [
                            "F4",
                        ],
                    },
                ),
            ],
        )

    def test_first_choice(self):
        self.assertEqual(
            first_choice(
                (
                    ("first", "First"),
                    ("second", "Second"),
                )
            ),
            "first",
        )

        self.assertEqual(
            first_choice(
                (
                    (
                        "Section 1",
                        (
                            ("first", "First"),
                            ("second", "Second"),
                        ),
                    ),
                ),
            ),
            "first",
        )

        self.assertEqual(
            first_choice(
                (
                    (
                        "Section 1",
                        (),
                    ),
                    (
                        "Section 2",
                        (
                            ("second", "Second"),
                            ("third", "Third"),
                        ),
                    ),
                )
            ),
            "second",
        )

    def test_link_to_framework(self):
        self.assertIsNone(link_to_framework_doc("Card", "this topic does not exist"))
        self.assertIsNone(
            link_to_framework_doc("NonExistingUIITEM", "this topic does not exist")
        )
