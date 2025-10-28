from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, MarginMixin, ResponsiveMixin
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
    text_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-image" '
        'viewBox="0 0 16 16"><path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>'
        '<path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2zm12 1a1 1 0 0 1 1 '
        "1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 "
        '1-1z"/></svg>'
    )

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
                    "alignment",
                ),
            },
        ),
        (
            _("Sizing"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("width", "height"),
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
        # assign link to a context variable to be performant
        context["picture_link"] = instance.get_link()
        context["picture_size"] = instance.get_size(
            width=context.get("width", 0),
            height=context.get("height", 0),
        )
        context["img_srcset_data"] = instance.img_srcset_data
        if instance.config.get("lazy_loading", False):
            instance.add_attribute("loading", "lazy")
        return super().render(context, instance, placeholder)
