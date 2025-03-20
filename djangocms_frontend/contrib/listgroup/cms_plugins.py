from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, MarginMixin, PaddingMixin, ResponsiveMixin
from .. import listgroup
from . import forms, models

mixin_factory = settings.get_renderer(listgroup)


@plugin_pool.register_plugin
class ListGroupPlugin(
    mixin_factory("ListGroup"),
    AttributesMixin,
    ResponsiveMixin,
    MarginMixin,
    CMSUIPlugin,
):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List group")
    module = _("Frontend")
    model = models.ListGroup
    form = forms.ListGroupForm
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    child_classes = ["ListGroupItemPlugin", "TextLinkPlugin"]
    show_add_form = False
    # TODO consider linking to tab-content

    fieldsets = [
        (None, {"fields": ("list_group_flush",)}),
    ]


@plugin_pool.register_plugin
class ListGroupItemPlugin(
    mixin_factory("ListGroupItem"),
    AttributesMixin,
    ResponsiveMixin,
    PaddingMixin,
    CMSUIPlugin,
):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List item")
    module = _("Frontend")
    model = models.ListGroupItem
    form = forms.ListGroupItemForm
    change_form_template = "djangocms_frontend/admin/list-group.html"
    allow_children = True
    parent_classes = ["ListGroupPlugin"]
    frontend_editable_fields = ("simple_content",)

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "simple_content",
                    "list_context",
                    "list_state",
                )
            },
        ),
    ]
