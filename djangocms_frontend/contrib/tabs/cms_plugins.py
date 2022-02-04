from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template

from ... import settings
from .. import tabs
from . import forms, models
from .constants import TAB_TEMPLATE_CHOICES

mixin_factory = settings.get_renderer(tabs)


@plugin_pool.register_plugin
class TabPlugin(mixin_factory("Tab"), CMSPluginBase):
    """
    Components > "Navs - Tab" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    name = _("Tabs")
    module = _("Frontend")
    model = models.Tab
    form = forms.TabForm
    change_form_template = "djangocms_frontend/admin/tabs.html"
    allow_children = True
    child_classes = ["TabItemPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("tab_type", "tab_alignment"),
                    ("tab_index", "tab_effect"),
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "template",
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "tabs", "tabs", TAB_TEMPLATE_CHOICES)


@plugin_pool.register_plugin
class TabItemPlugin(mixin_factory("TabItem"), CMSPluginBase):
    """
    Components > "Navs - Tab Item" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    name = _("Tab item")
    module = _("Frontend")
    model = models.TabItem
    form = forms.TabItemForm
    change_form_template = "djangocms_frontend/admin/tabs.html"
    allow_children = True
    parent_classes = ["TabPlugin"]

    fieldsets = [
        (
            None,
            {"fields": ("tab_title",)},
        ),
        (
            _("Tab item border"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tab_bordered",
                    "tab_padding_size",
                    "tab_padding_side",
                ),
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

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance.parent.get_plugin_instance()[0],
            "tabs",
            "item",
            TAB_TEMPLATE_CHOICES,
        )
