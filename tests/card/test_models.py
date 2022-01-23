from django.test import TestCase

from djangocms_frontend.contrib.card.models import (
    Card, CardInner,
)


class CardModelTestCase(TestCase):

    def test_card_instance(self):
        instance = Card.objects.create()
        self.assertEqual(str(instance), "Card (1)")
        self.assertEqual(instance.get_short_description(), "(card)")
        instance.card_context = "primary"
        self.assertEqual(instance.get_short_description(), "(card) .bg-primary")
        instance.card_outline = True
        self.assertEqual(instance.get_short_description(), "(card) .border-primary")
        instance.card_alignment = "center"
        self.assertEqual(instance.get_short_description(), "(card) .border-primary .center")

    def test_card_inner_instance(self):
        instance = CardInner.objects.create()
        self.assertEqual(str(instance), "CardInner (1)")
        self.assertEqual(instance.get_short_description(), "(card-body)")
