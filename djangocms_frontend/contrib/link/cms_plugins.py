from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template

from ... import settings
from .. import link
from . import forms, models
from .constants import USE_LINK_ICONS

mixin_factory = settings.get_renderer(link)


UILINK_FIELDS = (
    ("name", "link_type"),
    ("external_link", "internal_link"),
    ("link_context", "link_size"),
    ("link_outline", "link_block"),
)

UILINK_FIELDSET = [
    (
        None,
        {
            "fields": UILINK_FIELDS + (("icon_left", "icon_right"),)
            if USE_LINK_ICONS
            else UILINK_FIELDS
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


@plugin_pool.register_plugin
class LinkPlugin(mixin_factory("Link"), CMSPluginBase):
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

    fieldsets = UILINK_FIELDSET + [
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "template",
                    "attributes",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "link", "link", settings.LINK_TEMPLATE_CHOICES
        )
