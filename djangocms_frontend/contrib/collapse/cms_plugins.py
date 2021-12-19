from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from .models import (
    Bootstrap5Collapse,
    Bootstrap5CollapseContainer,
    Bootstrap5CollapseTrigger,
)


class Bootstrap5CollapsePlugin(CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    model = Bootstrap5Collapse
    name = _("Collapse")
    module = _("Interface")
    render_template = "djangocms_frontend/collapse.html"
    change_form_template = "djangocms_frontend/admin/collapse.html"
    allow_children = True
    child_classes = [
        "Bootstrap5CollapseTriggerPlugin",
        "Bootstrap5CollapseContainerPlugin",
        "Bootstrap5LinkPlugin",
        "Bootstrap5CardPlugin",
        "Bootstrap5SpacingPlugin",
        "Bootstrap5GridRowPlugin",
    ]

    fieldsets = [
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "siblings",
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]


class Bootstrap5CollapseTriggerPlugin(CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    model = Bootstrap5CollapseTrigger
    name = _("Collapse trigger")
    module = _("Bootstrap 5")
    render_template = "djangocms_frontend/collapse-trigger.html"
    allow_children = True
    parent_classes = [
        "Bootstrap5CardPlugin",
        "Bootstrap5CardInnerPlugin",
        "Bootstrap5CollapsePlugin",
        "Bootstrap5GridColumnPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("identifier",)}),
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


class Bootstrap5CollapseContainerPlugin(CMSPluginBase):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    model = Bootstrap5CollapseContainer
    name = _("Collapse container")
    module = _("Bootstrap 5")
    render_template = "djangocms_frontend/collapse-container.html"
    allow_children = True
    parent_classes = [
        "Bootstrap5CardPlugin",
        "Bootstrap5CardInnerPlugin",
        "Bootstrap5CollapsePlugin",
        "Bootstrap5GridColumnPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("identifier",)}),
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


plugin_pool.register_plugin(Bootstrap5CollapsePlugin)
plugin_pool.register_plugin(Bootstrap5CollapseTriggerPlugin)
plugin_pool.register_plugin(Bootstrap5CollapseContainerPlugin)
