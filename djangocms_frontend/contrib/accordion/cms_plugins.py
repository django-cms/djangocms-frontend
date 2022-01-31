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
    module = _("Frontend")
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
                    "create",
                    (
                        "accordion_header_type",
                        "accordion_flush",
                    ),
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for x in range(data["create"] if data["create"] is not None else 0):
            item = models.AccordionItem(
                parent=obj,
                placeholder=obj.placeholder,
                language=obj.language,
                position=obj.numchild,
                plugin_type=AccordionItemPlugin.__name__,
                ui_item=models.AccordionItem.__class__.__name__,
                config=dict(
                    accordion_item_header=_("Item {}").format(x + 1),
                    accordion_item_open=(x == 0),
                ),
            ).initialize_from_form(forms.AccordionItemForm)
            obj.add_child(instance=item)


@plugin_pool.register_plugin
class AccordionItemPlugin(mixin_factory("AccordionItem"), CMSPluginBase):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Accordion item")
    module = _("Frontend")
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
