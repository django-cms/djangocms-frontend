import copy

import cms.exceptions
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import image
from . import forms, models

mixin_factory = settings.get_renderer(image)


@plugin_pool.register_plugin
class ImagePlugin(mixin_factory("Image"), CMSPluginBase):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    name = _("Picture / Image")
    module = _("Frontend")

    model = models.Image
    form = forms.ImageForm

    change_form_template = "djangocms_frontend/admin/image.html"

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "picture",
                    "external_picture",
                    ("picture_fluid", "picture_rounded", "picture_thumbnail"),
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "template",
                    "use_responsive_image",
                    ("width", "height"),
                    "alignment",
                    "caption_text",
                    "attributes",
                ),
            },
        ),
        (
            _("Link settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    (
                        "external_link",
                        "internal_link",
                    ),
                    "file_link",
                ),
            },
        ),
        (
            _("Cropping settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("use_automatic_scaling", "use_no_cropping"),
                    ("use_crop", "use_upscale"),
                    "thumbnail_options",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return f"djangocms_frontend/{settings.framework}/{instance.template}/image.html"
