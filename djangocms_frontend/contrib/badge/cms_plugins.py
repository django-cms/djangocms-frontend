from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class BadgePlugin(CMSPluginBase):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    name = _("Badge")
    module = _("Interface")
    model = models.Badge
    form = forms.BadgeForm
    render_template = f"djangocms_frontend/{settings.framework}/badge.html"
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
        (_("Advanced settings"), {"classes": ("collapse",), "fields": ("attributes",)}),
    ]

    def render(self, context, instance, placeholder):
        link_classes = ["badge"]
        if instance.badge_pills:
            link_classes.append("badge-pill")
        link_classes.append("badge-{}".format(instance.badge_context))

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
