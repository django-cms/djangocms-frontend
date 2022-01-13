from functools import cached_property

from django.conf import settings
from django.utils.translation import gettext as _
from easy_thumbnails.files import get_thumbnailer
from entangled.utils import get_related_object

from djangocms_frontend.contrib.link.models import GetLinkMixin
from djangocms_frontend.models import FrontendUIItem

# use golden ration as default (https://en.wikipedia.org/wiki/Golden_ratio)
PICTURE_RATIO = getattr(settings, "DJANGOCMS_PICTURE_RATIO", 1.6180)


class PictureMixin:
    def get_size(self, width=None, height=None):
        crop = getattr(self, "use_crop", False)
        upscale = getattr(self, "use_upscale", False)
        # use field thumbnail settings
        if getattr(self, "thumbnail_options", None):
            thumbnail_options = get_related_object(self.config, "thumbnail_options")
            width = thumbnail_options.width
            height = thumbnail_options.height
            crop = thumbnail_options.crop
            upscale = thumbnail_options.upscale
        elif not getattr(self, "use_automatic_scaling", None):
            width = getattr(self, "width", None)
            height = getattr(self, "height", None)

        # calculate height when not given according to the
        # golden ratio or fallback to the picture size
        if not height and width:
            height = int(width / PICTURE_RATIO)
        elif not width and height:
            width = int(height * PICTURE_RATIO)
        elif not width and not height and getattr(self, "picture", None):
            picture = get_related_object(self.config, "picture")
            width = int(picture.width)
            height = int(picture.height)

        return {
            "size": (width, height),
            "crop": crop,
            "upscale": upscale,
        }


class Picture(GetLinkMixin, PictureMixin, FrontendUIItem):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    class Meta:
        proxy = True

    @cached_property
    def image(self):
        if self.picture:
            return get_related_object(self.config, "picture")
        return None

    @property
    def is_responsive_image(self):
        if self.external_picture:
            return False
        if self.use_responsive_image == "inherit":
            return getattr(settings, "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES", False)
        return self.use_responsive_image == "yes"

    @cached_property
    def img_srcset_data(self):
        if not (self.picture and self.is_responsive_image):
            return None

        srcset = []
        thumbnailer = get_thumbnailer(get_related_object(self.config, "picture"))
        picture_options = self.get_size(self.width, self.height)
        picture_width = picture_options["size"][0]
        thumbnail_options = {"crop": picture_options["crop"]}
        breakpoints = getattr(
            settings,
            "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS",
            [576, 768, 992],
        )

        for size in filter(lambda x: x < picture_width, breakpoints):
            thumbnail_options["size"] = (size, size)
            srcset.append((int(size), thumbnailer.get_thumbnail(thumbnail_options)))

        return srcset

    @cached_property
    def img_src(self):
        # we want the external picture to take priority by design
        # please open a ticket if you disagree for an open discussion
        if self.external_picture:
            return self.external_picture
        # picture can be empty, for example when the image is removed from filer
        # in this case we want to return an empty string to avoid #69
        elif not self.picture:
            return ""
        # return the original, unmodified picture
        elif self.use_no_cropping:
            return get_related_object(self.config, "picture").url

        picture_options = self.get_size(
            width=self.width or 0,
            height=self.height or 0,
        )

        thumbnail_options = {
            "size": picture_options["size"],
            "crop": picture_options["crop"],
            "upscale": picture_options["upscale"],
            "subject_location": get_related_object(
                self.config, "picture"
            ).subject_location,
        }

        thumbnailer = get_thumbnailer(get_related_object(self.config, "picture"))
        return thumbnailer.get_thumbnail(thumbnail_options).url

    def get_short_description(self):
        if self.external_picture:
            return self.external_picture
        if self.image and self.image.label:
            return self.image.label
        return _("<file is missing>")
