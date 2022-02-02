from django.test import TestCase

from djangocms_frontend.contrib.card.forms import CardForm, CardInnerForm
from djangocms_frontend.contrib.card.models import Card, CardInner


class CardModelTestCase(TestCase):
    def test_card_instance(self):
        instance = Card.objects.create().initialize_from_form(CardForm)
        self.assertEqual(str(instance), "Card (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.card_context = "primary"
        self.assertEqual(instance.get_short_description(), ".bg-primary")
        instance.card_outline = True
        self.assertEqual(instance.get_short_description(), ".border-primary")
        instance.card_alignment = "center"
        self.assertEqual(instance.get_short_description(), ".border-primary .center")

    def test_card_inner_instance(self):
        instance = CardInner.objects.create().initialize_from_form(CardInnerForm)
        self.assertEqual(str(instance), "CardInner (1)")
        self.assertEqual(instance.get_short_description(), "(body)")
