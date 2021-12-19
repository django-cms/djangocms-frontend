import os

from cms.models import CMSPlugin
from django import forms
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from djangocms_link.models import AbstractLink
from djangocms_text_ckeditor.fields import HTMLFormField
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminImageFormField

from djangocms_frontend.fields import AttributesField, TagTypeField

from ... import settings
from .constants import (
    CAROUSEL_ASPECT_RATIO_CHOICES,
    CAROUSEL_PAUSE_CHOICES,
    CAROUSEL_RIDE_CHOICES,
    CAROUSEL_TEMPLATE_CHOICES,
)


class CarouselForm(EntangledModelForm):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    template = forms.ChoiceField(
        label=_("Template"),
        choices=CAROUSEL_TEMPLATE_CHOICES,
        initial=CAROUSEL_TEMPLATE_CHOICES[0][0],
        help_text=_("This is the template that will be used for the component."),
    )
    carousel_interval = forms.IntegerField(
        label=_("Interval"),
        initial=5000,
        help_text=_(
            "The amount of time to delay between automatically cycling "
            "an item. If false, carousel will not automatically cycle."
        ),
    )
    carousel_controls = forms.BooleanField(
        label=_("Controls"),
        initial=True,
        required=False,
        help_text=_("Adding in the previous and next controls."),
    )
    carousel_indicators = forms.BooleanField(
        label=_("Indicators"),
        initial=True,
        required=False,
        help_text=_("Adding in the indicators to the carousel."),
    )
    carousel_keyboard = forms.BooleanField(
        label=_("Keyboard"),
        initial=True,
        help_text=_("Whether the carousel should react to keyboard events."),
    )
    carousel_pause = forms.ChoiceField(
        label=_("Pause"),
        choices=CAROUSEL_PAUSE_CHOICES,
        default=CAROUSEL_PAUSE_CHOICES[0][0],
        help_text=_(
            'If set to "hover", pauses the cycling of the carousel on '
            '"mouseenter" and resumes the cycling of the carousel on '
            '"mouseleave". If set to "false", hovering over the carousel '
            "won't pause it."
        ),
    )
    carousel_ride = forms.ChoiceField(
        label=_("Ride"),
        choices=CAROUSEL_RIDE_CHOICES,
        initial=CAROUSEL_RIDE_CHOICES[0][0],
        help_text=_(
            "Autoplays the carousel after the user manually cycles the "
            'first item. If "carousel", autoplays the carousel on load.'
        ),
    )
    carousel_wrap = forms.BooleanField(
        label=_("Wrap"),
        initial=True,
        required=False,
        help_text=_(
            "Whether the carousel should cycle continuously or have " "hard stops."
        ),
    )
    carousel_aspect_ratio = forms.ChoiceField(
        label=_("Aspect ratio"),
        choices=settings.EMPTY_CHOICE + CAROUSEL_ASPECT_RATIO_CHOICES,
        required=False,
        initial=settings.EMPTY_CHOICE[0][0],
        help_text=_(
            "Determines width and height of the image "
            "according to the selected ratio."
        ),
    )


class CarouselSlide(AbstractLink):
    """
    Components > "Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    carousel_image = AdminImageFormField(
        label=_("Slide image"),
    )
    carousel_content = HTMLFormField(
        label=_("Content"),
        required=False,
        initial="",
        help_text=_("Content may also be added using child plugins."),
    )
    tag_type = TagTypeField()

    def __str__(self):
        return str(self.pk)

    def clean(self):
        super(AbstractLink, self).clean()

    def get_link(self):
        return AbstractLink.get_link(self)

    def get_short_description(self):
        image_text = content_text = ""

        if self.carousel_image_id:
            if self.carousel_image.name:
                image_text = self.carousel_image.name
            elif (
                self.carousel_image.original_filename
                and os.path.split(self.carousel_image.original_filename)[1]
            ):
                image_text = os.path.split(self.carousel_image.original_filename)[1]
            else:
                image_text = "Image"
        if self.carousel_content:
            text = strip_tags(self.carousel_content).strip()
            if len(text) > 100:
                content_text = "{}...".format(text[:100])
            else:
                content_text = "{}".format(text)

        if image_text and content_text:
            return "{} ({})".format(image_text, content_text)
        else:
            return image_text or content_text
