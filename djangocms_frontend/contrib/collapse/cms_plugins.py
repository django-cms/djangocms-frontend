from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin
from .. import collapse
from . import forms, models

mixin_factory = settings.get_renderer(collapse)


@plugin_pool.register_plugin
class CollapsePlugin(mixin_factory("Collapse"), AttributesMixin, CMSUIPlugin):
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
        (None, {"fields": ("collapse_siblings",)}),
    ]


@plugin_pool.register_plugin
class CollapseTriggerPlugin(mixin_factory("CollapseTrigger"), AttributesMixin, CMSUIPlugin):
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
    ]


@plugin_pool.register_plugin
class CollapseContainerPlugin(mixin_factory("CollapseContainer"), AttributesMixin, CMSUIPlugin):
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
    ]
