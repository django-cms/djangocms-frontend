from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.files import get_thumbnailer

from djangocms_frontend.contrib.link.models import GetLinkMixin
from djangocms_frontend.helpers import get_related_object
from djangocms_frontend.models import FrontendUIItem

# use golden ration as default (https://en.wikipedia.org/wiki/Golden_ratio)
PICTURE_RATIO = getattr(settings, "DJANGOCMS_PICTURE_RATIO", 1.6180)


class ImageMixin:
    image_field = None

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
        else:
            width = getattr(self, "width", None)
            height = getattr(self, "height", None)

        # calculate height when not given according to the
        # golden ratio or fallback to the image size
        picture_ratio = self.rel_image.width / self.rel_image.height if self.rel_image else PICTURE_RATIO
        if not height and width:
            height = width / picture_ratio
        elif not width and height:
            width = height * picture_ratio
        elif not width and not height and getattr(self, "picture", None):
            if self.rel_image:
                width = self.rel_image.width
                height = self.rel_image.height
            else:
                width = 0
                height = 0
        elif not width and not height:  # pragma: no cover
            # If no information is available on the image size whatsoever,
            # make it 640px wide and use PICTURE_RATIO
            width, height = 640, 640 / PICTURE_RATIO
        width = int(width)
        height = int(height)
        return {
            "size": (width, height),
            "crop": crop,
            "upscale": upscale,
        }

    @cached_property
    def rel_image(self):
        if self.config.get(self.image_field, None):
            return get_related_object(self.config, self.image_field)
        return None


class Image(GetLinkMixin, ImageMixin, FrontendUIItem):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    class Meta:
        proxy = True
        verbose_name = _("Image")

    image_field = "picture"

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

        try:
            thumbnailer = get_thumbnailer(self.rel_image)

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
        except ValueError:
            # get_thumbnailer() raises this if it can't establish a `relative_name`.
            # This may mean that the filer image has been deleted
            pass

        return srcset

    @cached_property
    def img_src(self):
        # we want the external image to take priority by design
        # please open a ticket if you disagree for an open discussion
        if self.external_picture:
            return self.external_picture
        # image can be empty, for example when the image is removed from filer
        # in this case we want to return an empty string to avoid #69
        elif not self.picture:
            return ""
        # skip image processing when there's no width or height defined,
        # or when legacy use_no_cropping flag is present
        elif getattr(self, "use_no_cropping", None) or not (self.width or self.height):
            return self.rel_image.url if self.rel_image else ""

        picture_options = self.get_size(
            width=self.width or 0,
            height=self.height or 0,
        )

        thumbnail_options = {
            "size": picture_options["size"],
            "crop": picture_options["crop"],
            "upscale": picture_options["upscale"],
            "subject_location": self.rel_image.subject_location if self.rel_image else (),
        }

        try:
            thumbnailer = get_thumbnailer(self.rel_image)
            url = thumbnailer.get_thumbnail(thumbnail_options).url
        except ValueError:
            # get_thumbnailer() raises this if it can't establish a `relative_name`.
            # This may mean that the filer image has been deleted
            url = ""
        return url

    def get_short_description(self):
        if self.external_picture:
            return self.external_picture
        if self.rel_image and self.rel_image.label:
            return self.rel_image.label
        return _("<file is missing>")
