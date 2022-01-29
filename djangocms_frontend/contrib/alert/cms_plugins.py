from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import alert
from . import forms, models

mixin_factory = settings.get_renderer(alert)


@plugin_pool.register_plugin
class AlertPlugin(mixin_factory("Alert"), CMSPluginBase):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    name = _("Alert")
    module = _("Frontend")
    model = models.Alert
    form = forms.AlertForm
    render_template = f"djangocms_frontend/{settings.framework}/alert.html"
    change_form_template = "djangocms_frontend/admin/alert.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "alert_context",
                    "alert_dismissible",
                ]
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
