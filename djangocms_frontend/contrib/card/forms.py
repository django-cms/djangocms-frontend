from copy import copy

from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import COLOR_STYLE_CHOICES, DEVICE_SIZES

from ... import settings
from ...fields import AttributesFormField, ColoredButtonGroup
from ...helpers import first_choice, link_to_framework_doc
from ...models import FrontendUIItem
from .. import card
from ..grid.constants import GRID_SIZE
from ..grid.forms import GridColumnForm
from .constants import (
    CARD_ALIGNMENT_CHOICES,
    CARD_INNER_TYPE_CHOICES,
    CARD_LAYOUT_TYPE_CHOICES,
)

# card allow for a transparent color
CARD_COLOR_STYLE_CHOICES = settings.COLOR_STYLE_CHOICES + (
    ("transparent", _("Transparent")),
)

CARD_TEXT_STYLES = COLOR_STYLE_CHOICES + (("white", _("White")),)

mixin_factory = settings.get_forms(card)


class CardLayoutBaseForm(mixin_factory("CardLayout"), EntangledModelForm):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "card_type",
                "attributes",
            ]
        }
        untangled_fields = (
            "tag_type",
            "create",
        )
        css = settings.ADMIN_CSS

    create = forms.IntegerField(
        label=_("Create cards"),
        help_text=_("Number of cards to create when saving."),
        required=False,
        min_value=0,
        max_value=100,
    )
    card_type = forms.ChoiceField(
        label=_("Card type"),
        choices=CARD_LAYOUT_TYPE_CHOICES,
        initial=first_choice(CARD_LAYOUT_TYPE_CHOICES),
        help_text=link_to_framework_doc("CardLayout", "card_type_link"),
    )
    attributes = AttributesFormField()


extra_fields_row_cols = {}
for size in settings.DEVICE_SIZES:
    extra_fields_row_cols["row_cols_{}".format(size)] = forms.IntegerField(
        label="row-cols" if size == "xs" else "row-cols-{}".format(size),
        required=False,
        min_value=1,
        max_value=GRID_SIZE,
    )

CardLayoutForm = type(
    str("CardLayoutBaseForm"),
    (CardLayoutBaseForm,),
    copy(extra_fields_row_cols),
)

CardLayoutForm.Meta.entangled_fields["config"] += extra_fields_row_cols.keys()


class CardForm(mixin_factory("Card"), EntangledModelForm):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "card_context",
                "card_alignment",
                "card_outline",
                "card_text_color",
                "card_full_height",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)
        css = settings.ADMIN_CSS

    card_context = forms.ChoiceField(
        label=_("Background context"),
        choices=settings.EMPTY_CHOICE + CARD_COLOR_STYLE_CHOICES,
        widget=ColoredButtonGroup(),
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
    card_full_height = forms.BooleanField(
        label=_("Full height"),
        initial=False,
        required=False,
        help_text=_(
            "If checked cards in one row will automatically extend to the full row height."
        ),
    )
    attributes = AttributesFormField()


class CardInnerForm(mixin_factory("CardInner"), EntangledModelForm):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "inner_type",
                "inner_context",
                "text_alignment",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    inner_type = forms.ChoiceField(
        label=_("Inner type"),
        choices=CARD_INNER_TYPE_CHOICES,
        initial=CARD_INNER_TYPE_CHOICES[0][0],
        help_text=_("Define the structure of the plugin."),
    )
    inner_context = forms.ChoiceField(
        label=_("Background context"),
        choices=settings.EMPTY_CHOICE + CARD_COLOR_STYLE_CHOICES,
        widget=ColoredButtonGroup(),
        required=False,
    )
    text_alignment = forms.ChoiceField(
        label=_("Content alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()


class CardDeckBaseForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    attributes = AttributesFormField()


extra_fields_column = {}
for size in DEVICE_SIZES:
    extra_fields_column["{}_cards".format(size)] = forms.IntegerField(
        label="col" if size == "xs" else "col-{}".format(size),
        required=False,
        min_value=1,
        max_value=GRID_SIZE,
    )

CardDeckForm = type(
    str("CardDeckBaseForm"),
    (CardDeckBaseForm,),
    copy(extra_fields_column),
)

CardDeckForm.Meta.entangled_fields["config"] += extra_fields_column.keys()
