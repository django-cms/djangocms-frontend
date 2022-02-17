from django.test import TestCase

from djangocms_frontend.contrib.card.forms import CardForm, CardInnerForm
from djangocms_frontend.contrib.card.models import Card, CardInner


class CardModelTestCase(TestCase):
    def test_card_instance(self):
        instance = Card.objects.create().initialize_from_form(CardForm)
        self.assertEqual(str(instance), "Card (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.config["background_context"] = "primary"
        self.assertEqual(instance.get_short_description(), ".bg-primary")
        instance.config["card_outline"] = "secondary"
        self.assertEqual(
            instance.get_short_description(), ".bg-primary .border-secondary"
        )
        instance.card_alignment = "center"
        self.assertEqual(
            instance.get_short_description(), ".bg-primary .border-secondary .center"
        )

    def test_card_inner_instance(self):
        instance = CardInner.objects.create().initialize_from_form(CardInnerForm)
        self.assertEqual(str(instance), "CardInner (1)")
        self.assertEqual(instance.get_short_description(), "(body)")
