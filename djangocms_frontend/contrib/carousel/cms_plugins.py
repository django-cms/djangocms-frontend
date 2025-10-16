from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, BackgroundMixin
from .. import carousel
from ..link.cms_plugins import LinkPluginMixin
from . import forms, models
from .constants import CAROUSEL_TEMPLATE_CHOICES

mixin_factory = settings.get_renderer(carousel)


@plugin_pool.register_plugin
class CarouselPlugin(mixin_factory("Carousel"), AttributesMixin, CMSUIPlugin):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    name = _("Carousel")
    module = _("Frontend")
    model = models.Carousel
    form = forms.CarouselForm
    allow_children = True
    child_classes = ["CarouselSlidePlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    ("carousel_aspect_ratio", "carousel_interval"),
                    ("carousel_controls", "carousel_indicators"),
                    ("carousel_keyboard", "carousel_wrap"),
                    ("carousel_ride",),
                    (
                        "carousel_transition",
                        "carousel_pause",
                    ),
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "carousel", "carousel", CAROUSEL_TEMPLATE_CHOICES)


@plugin_pool.register_plugin
class CarouselSlidePlugin(
    mixin_factory("CarouselSlide"),
    AttributesMixin,
    BackgroundMixin,
    LinkPluginMixin,
    CMSUIPlugin,
):
    """
    Components > "Carousel Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    name = _("Carousel slide")
    module = _("Frontend")
    model = models.CarouselSlide
    form = forms.CarouselSlideForm
    allow_children = True
    parent_classes = ["CarouselPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "carousel_image",
                    "carousel_content",
                )
            },
        ),
    ]
    link_fieldset_position = 1

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance.parent.get_plugin_instance()[0] if instance.parent else instance,
            # instance.parent or instance once django-cms 4.1 support can be dropped
            "carousel",
            "slide",
            CAROUSEL_TEMPLATE_CHOICES,
        )
