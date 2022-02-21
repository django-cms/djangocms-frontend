from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.spacing import SpacingMixin
from .. import link
from . import forms, models
from .constants import USE_LINK_ICONS

mixin_factory = settings.get_renderer(link)


UILINK_FIELDS = (
    ("name", "link_type"),
    ("external_link", "internal_link"),
    ("link_context", "link_size"),
    ("link_outline", "link_block"),
    "link_stretched",
)

UILINK_FIELDSET = [
    (
        None,
        {
            "fields": ("template",)
            + (
                UILINK_FIELDS + (("icon_left", "icon_right"),)
                if USE_LINK_ICONS
                else UILINK_FIELDS
            )
        },
    ),
    (
        _("Link settings"),
        {
            "classes": ("collapse",),
            "fields": (
                ("mailto", "phone"),
                ("anchor", "target"),
                ("file_link",),
            ),
        },
    ),
]


class LinkPluginMixin:
    def get_form(self, request, obj=None, change=False, **kwargs):
        """The link form needs the request object to check permissions"""
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form


@plugin_pool.register_plugin
class LinkPlugin(
    mixin_factory("Link"), AttributesMixin, SpacingMixin, LinkPluginMixin, CMSUIPlugin
):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    name = _("Link / Button")
    module = _("Frontend")
    model = models.Link
    form = forms.LinkForm
    change_form_template = "djangocms_frontend/admin/link.html"
    text_enabled = True
    allow_children = True

    fieldsets = UILINK_FIELDSET

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "link", "link", settings.LINK_TEMPLATE_CHOICES
        )
