from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.background import BackgroundMixin
from ...common.responsive import ResponsiveMixin
from ...common.spacing import SpacingMixin
from .. import icon
from . import forms, models

mixin_factory = settings.get_renderer(icon)


class IconPlugin(
    mixin_factory("Icon"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Universal icon picker
    https://github.com/migliori/universal-icon-picker
    """

    name = _("Icon")
    module = _("Frontend")
    model = models.Icon
    form = forms.IconForm
    text_enabled = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "icon",
                        "icon_size",
                    ),
                    "icon_foreground",
                    "icon_rounded",
                )
            },
        ),
    ]


if "IconPlugin" in plugin_pool.plugins:
    #  Unregister already installed IconPlugin
    del plugin_pool.plugins["IconPlugin"]

plugin_pool.register_plugin(IconPlugin)
