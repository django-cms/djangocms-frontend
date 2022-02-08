from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from .. import collapse
from . import forms, models

mixin_factory = settings.get_renderer(collapse)


@plugin_pool.register_plugin
class CollapsePlugin(mixin_factory("Collapse"), CMSUIPlugin):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse")
    module = _("Frontend")
    model = models.Collapse
    form = forms.CollapseForm
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
class CollapseTriggerPlugin(mixin_factory("CollapseTrigger"), CMSUIPlugin):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse trigger")
    module = _("Frontend")
    model = models.CollapseTrigger
    form = forms.CollapseTriggerForm
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
class CollapseContainerPlugin(mixin_factory("CollapseContainer"), CMSUIPlugin):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Collapse container")
    module = _("Frontend")
    model = models.CollapseContainer
    form = forms.CollapseContainerForm
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
