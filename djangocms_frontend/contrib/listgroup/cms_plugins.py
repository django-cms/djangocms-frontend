from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import listgroup
from . import forms, models

mixin_factory = settings.get_renderer(listgroup)


@plugin_pool.register_plugin
class ListGroupPlugin(mixin_factory("ListGroup"), CMSPluginBase):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List group")
    module = _("Frontend")
    model = models.ListGroup
    form = forms.ListGroupForm
    render_template = f"djangocms_frontend/{settings.framework}/list-group.html"
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    child_classes = ["ListGroupItemPlugin", "LinkPlugin"]
    # TODO consider linking to tab-content

    fieldsets = [
        (None, {"fields": ("list_group_flush",)}),
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
class ListGroupItemPlugin(mixin_factory("ListGroupItem"), CMSPluginBase):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List item")
    module = _("Frontend")
    model = models.ListGroupItem
    form = forms.ListGroupItemForm
    render_template = f"djangocms_frontend/{settings.framework}/list-group-item.html"
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    parent_classes = ["ListGroupPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "list_context",
                    "list_state",
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
