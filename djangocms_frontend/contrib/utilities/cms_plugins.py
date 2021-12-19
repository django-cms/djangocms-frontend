from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings

from . import forms, models


@plugin_pool.register_plugin
class SpacingPlugin(CMSPluginBase):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Spacing")
    module = _("Interface")
    model = models.Spacing
    form = forms.SpacingForm

    render_template = f"{settings.framework}/spacing.html"
    change_form_template = "djangocms_frontend/admin/spacing.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "space_property",
                    "space_sides",
                    "space_size",
                    "space_device",
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]
