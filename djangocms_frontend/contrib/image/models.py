from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djangocms_picture.backends import RenditionSpec, get_backend
from djangocms_picture.rendering import build_srcset, calculate_size

from djangocms_frontend.contrib.link.models import GetLinkMixin
from djangocms_frontend.helpers import get_related_object
from djangocms_frontend.models import FrontendUIItem

from .fields import get_picture_reference

# use golden ratio as default (https://en.wikipedia.org/wiki/Golden_ratio)
PICTURE_RATIO = getattr(settings, "DJANGOCMS_PICTURE_RATIO", 1.6180)


class ImageMixin:
    image_field = None

    @cached_property
    def picture_reference(self):
        return get_picture_reference(
            self.config,
            self.image_field,
            external_field_name="external_picture" if self.image_field == "picture" else None,
        )

    @cached_property
    def picture_backend(self):
        reference = self.picture_reference
        if not reference:
            return None
        try:
            return get_backend(reference.backend)
        except (ImproperlyConfigured, KeyError, ValueError):
            return None

    @cached_property
    def image_asset(self):
        if not self.picture_backend or not self.picture_reference:
            return None
        return self.picture_backend.resolve(self.picture_reference)

    @cached_property
    def image_attribution(self):
        return self.image_asset.attribution if self.image_asset else None

    @property
    def image_alt_text(self):
        return self.image_asset.info.alt_text if self.image_asset else ""

    @cached_property
    def rel_image(self):
        """Compatibility facade for templates that still expect a model image."""

        return getattr(self.image_asset, "image", None) if self.image_asset else None

    def _related_preset(self, field_name):
        if not self.config.get(field_name):
            return None
        return get_related_object(self.config, field_name)

    def get_rendition_spec(self, width=None, height=None):
        crop = getattr(self, "use_crop", False)
        upscale = getattr(self, "use_upscale", False)
        backend = self.picture_backend

        thumbnail_options = self._related_preset("thumbnail_options")
        rendition_preset = self._related_preset("rendition_preset")
        if backend and backend.supports_configuration_field("thumbnail_options") and thumbnail_options:
            width = thumbnail_options.width
            height = thumbnail_options.height
            crop = thumbnail_options.crop
            upscale = thumbnail_options.upscale
        elif backend and backend.supports_configuration_field("rendition_preset") and rendition_preset:
            width = rendition_preset.width
            height = rendition_preset.height
            crop = rendition_preset.crop
            upscale = rendition_preset.upscale
        else:
            width = width or getattr(self, "width", None)
            height = height or getattr(self, "height", None)

        return calculate_size(
            self.image_asset.info if self.image_asset else None,
            width=width,
            height=height,
            crop=crop,
            upscale=upscale,
            picture_ratio=PICTURE_RATIO,
        )

    def get_size(self, width=None, height=None):
        spec = self.get_rendition_spec(width=width, height=height)
        return {
            "size": (spec.width, spec.height),
            "crop": spec.crop,
            "upscale": spec.upscale,
        }

    @cached_property
    def img_src(self):
        if not self.image_asset:
            return ""
        if getattr(self, "use_no_cropping", False):
            return self.image_asset.get_original().url

        has_transform = any(
            (
                getattr(self, "width", None),
                getattr(self, "height", None),
                self.config.get("thumbnail_options"),
                self.config.get("rendition_preset"),
            )
        )
        if not has_transform:
            return self.image_asset.get_original().url

        spec = self.get_rendition_spec()
        capabilities = self.picture_backend.capabilities
        return self.image_asset.get_rendition(
            RenditionSpec(
                width=spec.width,
                height=spec.height,
                crop=spec.crop and capabilities.crop,
                upscale=spec.upscale and capabilities.upscale,
            )
        ).url


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
    def external_picture(self):
        legacy_value = self.config.get("external_picture")
        if legacy_value:
            return legacy_value
        reference = self.picture_reference
        return reference.id if reference and reference.backend == "url" else ""

    @property
    def is_responsive_image(self):
        if not self.image_asset or not self.picture_backend.capabilities.responsive:
            return False
        if self.use_responsive_image == "inherit":
            return getattr(settings, "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES", False)
        return self.use_responsive_image == "yes"

    @cached_property
    def img_srcset_data(self):
        if not self.is_responsive_image:
            return None

        spec = self.get_rendition_spec(self.width, self.height)
        breakpoints = getattr(
            settings,
            "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS",
            [576, 768, 992],
        )
        return build_srcset(
            self.image_asset,
            widths=breakpoints,
            width=spec.width,
            height=spec.height,
            crop=spec.crop and self.picture_backend.capabilities.crop,
            upscale=spec.upscale and self.picture_backend.capabilities.upscale,
        )

    def get_short_description(self):
        if self.image_asset and self.image_asset.info.label:
            return self.image_asset.info.label
        return _("<file is missing>")
