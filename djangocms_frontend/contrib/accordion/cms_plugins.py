from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import accordion
from . import forms, models

mixin_factory = settings.get_renderer(accordion)


@plugin_pool.register_plugin
class AccordionPlugin(mixin_factory("Accordion"), CMSPluginBase):
    """
    Component > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    name = _("Accordion")
    module = _("Interface")
    model = models.Accordion
    form = forms.AccordionForm
    render_template = f"djangocms_frontend/{settings.framework}/accordion.html"
    # change_form_template = "djangocms_frontend/admin/collapse.html"
    allow_children = True
    child_classes = [
        "AccordionItemPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "accordion_header_type",
                    "accordion_flush",
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


@plugin_pool.register_plugin
class AccordionItemPlugin(mixin_factory("AccordionItem"), CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Accordion item")
    module = _("Interface")
    model = models.AccordionItem
    form = forms.AccordionItemForm
    render_template = f"djangocms_frontend/{settings.framework}/accordion_item.html"
    allow_children = True
    parent_classes = [
        "AccordionPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "accordion_item_header",
                    "accordion_item_open",
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
