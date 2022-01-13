import copy

import cms.exceptions
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class ImagePlugin(CMSPluginBase):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    name = _("Picture / Image")
    module = _("Interface")

    model = models.Picture
    form = forms.PictureForm

    change_form_template = "djangocms_frontend/admin/picture.html"

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
        return (
            f"djangocms_frontend/{settings.framework}/{instance.template}/picture.html"
        )

    def render(self, context, instance, placeholder):
        if instance.alignment:
            classes = "align-{} ".format(instance.alignment)
            classes += instance.attributes.get("class", "")
            # Set the class attribute to include the alignment html class
            # This is done to leverage the attributes_str property
            instance.attributes["class"] = classes
        # assign link to a context variable to be performant
        context["picture_link"] = instance.get_link()
        context["picture_size"] = instance.get_size(
            width=context.get("width", 0),
            height=context.get("height", 0),
        )
        context["img_srcset_data"] = instance.img_srcset_data
        link_classes = []
        if instance.picture_fluid:
            link_classes.append("img-fluid")
        if instance.picture_rounded:
            link_classes.append("rounded")
        if instance.picture_thumbnail:
            link_classes.append("img-thumbnail")

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
