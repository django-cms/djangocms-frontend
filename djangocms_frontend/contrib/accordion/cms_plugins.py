from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin
from ...helpers import add_plugin
from .. import accordion
from . import forms, models

mixin_factory = settings.get_renderer(accordion)


@plugin_pool.register_plugin
class AccordionPlugin(mixin_factory("Accordion"), AttributesMixin, CMSUIPlugin):
    """
    Component > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    name = _("Accordion")
    module = _("Frontend")
    model = models.Accordion
    form = forms.AccordionForm
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
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for pos in range(data["create"] if data["create"] is not None else 0):
            item = models.AccordionItem(
                parent=obj,
                position=obj.position + 1 + pos,
                placeholder=obj.placeholder,
                language=obj.language,
                plugin_type=AccordionItemPlugin.__name__,
                ui_item=models.AccordionItem.__class__.__name__,
                config=dict(
                    accordion_item_header=_("Item {}").format(pos + 1),
                    accordion_item_open=(pos == 0),
                ),
            ).initialize_from_form(forms.AccordionItemForm)
            add_plugin(obj.placeholder, item)


@plugin_pool.register_plugin
class AccordionItemPlugin(mixin_factory("AccordionItem"), CMSUIPlugin):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    name = _("Accordion item")
    module = _("Frontend")
    model = models.AccordionItem
    form = forms.AccordionItemForm
    allow_children = True
    show_add_form = False

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

    frontend_editable_fields = ("accordion_item_header",)
