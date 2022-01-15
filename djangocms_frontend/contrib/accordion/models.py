from django.utils.translation import gettext as _

from djangocms_frontend.models import FrontendUIItem


class Accordion(FrontendUIItem):
    """
    Components > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return _("({} entries)").format(self.get_children_count())


class AccordionItem(FrontendUIItem):
    """
    Components > "Accordion" Plugin
    https://getbootstrap.com/docs/5.0/components/accordion/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return getattr(self, "accordion_item_header", "-")
