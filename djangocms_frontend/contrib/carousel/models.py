import os
from functools import cached_property

from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from entangled.utils import get_related_object

from djangocms_frontend.models import FrontendUIItem

from ..link.models import GetLinkMixin


class Carousel(FrontendUIItem):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        text = "({})".format(self.template)
        text += " {}: {}".format(_("Interval"), self.carousel_interval)
        text += ", {}: {}".format(_("Controls"), self.carousel_controls)
        text += ", {}: {}".format(_("Indicators"), self.carousel_indicators)
        text += ", {}: {}".format(_("Keyboard"), self.carousel_keyboard)
        text += ", {}: {}".format(_("Pause"), self.carousel_pause)
        text += ", {}: {}".format(_("Ride"), self.carousel_ride)
        text += "{}: {}".format(_("Wrap"), self.carousel_wrap)
        return text


class CarouselSlide(GetLinkMixin, FrontendUIItem):
    """
    Components > "Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        proxy = True

    @cached_property
    def image(self):
        if self.carousel_image:
            return get_related_object(self.config, "carousel_image")
        return None

    def get_short_description(self):
        image_text = content_text = ""

        if self.carousel_image:
            if self.image is None:
                image_text = _("<file is missing>")
            elif self.image.name:
                image_text = self.image.name
            elif (
                self.image.original_filename
                and os.path.split(self.image.original_filename)[1]
            ):
                image_text = os.path.split(self.image.original_filename)[1]
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
