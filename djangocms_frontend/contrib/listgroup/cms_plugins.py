from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class ListGroupPlugin(CMSPluginBase):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List group")
    module = _("Interface")
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

    def render(self, context, instance, placeholder):
        link_classes = ["list-group"]
        if instance.list_group_flush:
            link_classes.append("list-group-flush")

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class ListGroupItemPlugin(CMSPluginBase):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    name = _("List item")
    module = _("Interface")
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

    def render(self, context, instance, placeholder):
        link_classes = ["list-group-item"]
        if instance.list_context:
            link_classes.append("list-group-item-{}".format(instance.list_context))
        if instance.list_state:
            link_classes.append(instance.list_state)

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
