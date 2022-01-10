from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class CollapsePlugin(CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse")
    module = _("Interface")
    model = models.Collapse
    form = forms.CollapseForm
    render_template = f"{settings.framework}/collapse.html"
    change_form_template = "djangocms_frontend/admin/collapse.html"
    allow_children = True
    child_classes = [
        "CollapseTriggerPlugin",
        "CollapseContainerPlugin",
        "LinkPlugin",
        "CardPlugin",
        "SpacingPlugin",
        "GridRowPlugin",
    ]

    fieldsets = [
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "collapse_siblings",
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]


@plugin_pool.register_plugin
class CollapseTriggerPlugin(CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse trigger")
    module = _("Interface")
    model = models.CollapseTrigger
    form = forms.CollapseTriggerForm
    render_template = f"djangocms_frontend/{settings.framework}/collapse-trigger.html"
    allow_children = True
    parent_classes = [
        "CardPlugin",
        "CardInnerPlugin",
        "CollapsePlugin",
        "GridColumnPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("trigger_identifier",)}),
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


@plugin_pool.register_plugin
class CollapseContainerPlugin(CMSPluginBase):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse container")
    module = _("Interface")
    model = models.CollapseContainer
    form = forms.CollapseContainerForm
    render_template = f"djangocms_frontend/{settings.framework}/collapse-container.html"
    allow_children = True
    parent_classes = [
        "CardPlugin",
        "CardInnerPlugin",
        "CollapsePlugin",
        "GridColumnPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("container_identifier",)}),
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
        classes = concat_classes(
            [
                "collapse",
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
