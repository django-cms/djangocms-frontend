from django.test import TestCase

from djangocms_frontend.contrib.accordion.forms import AccordionForm, AccordionItemForm
from djangocms_frontend.contrib.accordion.models import Accordion, AccordionItem


class AccordionModelTestCase(TestCase):
    def test_instance(self):
        instance = Accordion.objects.create()
        instance.initialize_from_form(AccordionForm).save()
        self.assertEqual(str(instance), "Accordion (1)")
        self.assertEqual(instance.get_short_description(), "(0 entries)")

        item = AccordionItem.objects.create()
        item.initialize_from_form(AccordionItemForm)
        item.config["accordion_item_header"] = "man-machine"
        self.assertEqual(str(item), "AccordionItem (2)")
        self.assertEqual(item.get_short_description(), "man-machine")
