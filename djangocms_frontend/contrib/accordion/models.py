from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Accordion(FrontendUIItem):
    """
    Components > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    class Meta:
        proxy = True
        verbose_name = _("Accordion")

    def get_short_description(self):
        return _("({} entries)").format(len(self.child_plugin_instances or []))


class AccordionItem(FrontendUIItem):
    """
    Components > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    _("AccordionItem")

    class Meta:
        proxy = True
        verbose_name = _("Accordion item")

    def get_short_description(self):
        return getattr(self, "accordion_item_header", "-")
