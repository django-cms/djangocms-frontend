import os

from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem

from ..image.models import ImageMixin
from ..link.models import GetLinkMixin


class Carousel(FrontendUIItem):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        proxy = True
        verbose_name = _("Carousel")

    def get_short_description(self):
        text = f"({self.template})"
        text += " {}: {}".format(_("Interval"), self.carousel_interval)
        text += ", {}: {}".format(_("Controls"), self.carousel_controls)
        text += ", {}: {}".format(_("Indicators"), self.carousel_indicators)
        text += ", {}: {}".format(_("Keyboard"), self.carousel_keyboard)
        text += ", {}: {}".format(_("Pause"), self.carousel_pause)
        text += ", {}: {}".format(_("Ride"), self.carousel_ride)
        text += ", {}: {}".format(_("Wrap"), self.carousel_wrap)
        return text


class CarouselSlide(GetLinkMixin, ImageMixin, FrontendUIItem):
    """
    Components > "Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        proxy = True
        verbose_name = _("Carousel slide")

    image_field = "carousel_image"

    def get_short_description(self):
        image_text = content_text = ""

        if self.carousel_image:
            if self.rel_image is None:
                image_text = _("<file is missing>")
            elif self.rel_image.name:
                image_text = self.rel_image.name
            elif self.rel_image.original_filename and os.path.split(self.rel_image.original_filename)[1]:
                image_text = os.path.split(self.rel_image.original_filename)[1]
            else:
                image_text = "Image"
        if self.carousel_content:
            text = strip_tags(self.carousel_content).strip()
            if len(text) > 100:
                content_text = f"{text[:100]}..."
            else:
                content_text = f"{text}"

        if image_text and content_text:
            return f"{image_text} ({content_text})"
        else:
            return image_text or content_text
