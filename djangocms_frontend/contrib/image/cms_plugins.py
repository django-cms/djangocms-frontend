from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.responsive import ResponsiveMixin
from ...common.spacing import MarginMixin
from .. import image
from ..link.cms_plugins import LinkPluginMixin
from . import forms, models

mixin_factory = settings.get_renderer(image)


@plugin_pool.register_plugin
class ImagePlugin(
    mixin_factory("Image"),
    AttributesMixin,
    ResponsiveMixin,
    MarginMixin,
    LinkPluginMixin,
    CMSUIPlugin,
):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    name = _("Picture / Image")
    module = _("Frontend")

    model = models.Image
    form = forms.ImageForm

    text_enabled = True

    change_form_template = "djangocms_frontend/admin/image.html"

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    "picture",
                    "external_picture",
                    (
                        "picture_fluid",
                        "lazy_loading",
                        "picture_rounded",
                        "picture_thumbnail",
                    ),
                )
            },
        ),
        (
            _("Format"),
            {
                "classes": ("collapse",),
                "fields": (
                    "use_responsive_image",
                    ("width", "height"),
                    "alignment",
                ),
            },
        ),
        (
            _("Cropping"),
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
    link_fieldset_position = -1

    def get_render_template(self, context, instance, placeholder):
        return f"djangocms_frontend/{settings.framework}/{instance.template}/image.html"

    def render(self, context, instance, placeholder):
        if instance.config.get("lazy_loading", False):
            instance.add_attribute("loading", "lazy")
        return super().render(context, instance, placeholder)
