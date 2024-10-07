from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin
from .. import badge
from . import forms, models

mixin_factory = settings.get_renderer(badge)


@plugin_pool.register_plugin
class BadgePlugin(mixin_factory("Badge"), AttributesMixin, CMSUIPlugin):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    name = _("Badge")
    module = _("Frontend")
    model = models.Badge
    form = forms.BadgeForm
    render_template = "djangocms_frontend/badge.html"
    change_form_template = "djangocms_frontend/admin/badge.html"
    text_enabled = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "badge_text",
                    "badge_context",
                    "badge_pills",
                )
            },
        ),
    ]
