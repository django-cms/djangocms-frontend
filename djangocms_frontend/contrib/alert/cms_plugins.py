from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class AlertPlugin(CMSPluginBase):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    name = _("Alert")
    module = _("Interface")
    model = models.Alert
    form = forms.AlertForm
    render_template = f"djangocms_frontend/{settings.framework}/alert.html"
    change_form_template = "djangocms_frontend/admin/alert.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "alert_context",
                    "alert_dismissable",
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

    def render(self, context, instance, placeholder):
        link_classes = ["alert"]
        link_classes.append("alert-{}".format(instance.alert_context))

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
