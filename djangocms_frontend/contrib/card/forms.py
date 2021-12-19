from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import COLOR_STYLE_CHOICES

from ... import settings
from ...models import FrontendUIItem
from .constants import (
    CARD_ALIGNMENT_CHOICES,
    CARD_INNER_TYPE_CHOICES,
    CARD_TYPE_CHOICES,
)

# card allow for a transparent color
CARD_COLOR_STYLE_CHOICES = COLOR_STYLE_CHOICES + (("transparent", _("Transparent")),)

CARD_TEXT_STYLES = COLOR_STYLE_CHOICES + (("white", _("White")),)


class CardForm(EntangledModelForm):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "card_type",
                "card_context",
                "card_alignment",
                "card_outline",
                "card_text_color",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    card_type = forms.ChoiceField(
        label=_("Card type"),
        choices=CARD_TYPE_CHOICES,
        initial=CARD_TYPE_CHOICES[0][0],
    )
    card_context = forms.ChoiceField(
        label=_("Background context"),
        choices=settings.EMPTY_CHOICE + CARD_COLOR_STYLE_CHOICES,
        required=False,
    )
    card_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + CARD_ALIGNMENT_CHOICES,
        required=False,
    )
    card_outline = forms.BooleanField(
        label=_("Outline"),
        initial=False,
        required=False,
        help_text=_("Uses the border context instead of the background."),
    )
    card_text_color = forms.ChoiceField(
        label=_("Text context"),
        choices=settings.EMPTY_CHOICE + CARD_TEXT_STYLES,
        required=False,
    )


class CardInnerForm(EntangledModelForm):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "inner_type",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    inner_type = forms.ChoiceField(
        label=_("Inner type"),
        choices=CARD_INNER_TYPE_CHOICES,
        initial=CARD_INNER_TYPE_CHOICES[0][0],
        help_text=_("Define the structure of the plugin."),
    )
