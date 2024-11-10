from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField, ColoredButtonGroup, TagTypeFormField

from ... import settings
from ...common import BackgroundFormMixin, ResponsiveFormMixin, SpacingFormMixin
from ...helpers import first_choice
from ...models import FrontendUIItem
from ...settings import COLOR_STYLE_CHOICES
from .conf import ICON_SIZE_CHOICES, ICON_TAG_TYPES
from .fields import IconPickerField


class IconForm(BackgroundFormMixin, ResponsiveFormMixin, SpacingFormMixin, EntangledModelForm):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "icon",
                "icon_size",
                "icon_foreground",
                "icon_rounded",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    icon = IconPickerField()
    icon_size = forms.ChoiceField(
        label=_("Icon size"),
        choices=ICON_SIZE_CHOICES,
        initial=first_choice(ICON_SIZE_CHOICES),
        required=False,
    )
    icon_foreground = forms.ChoiceField(
        label=_("Foreground context"),
        choices=settings.EMPTY_CHOICE + COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ColoredButtonGroup(),
        required=False,
    )
    icon_rounded = forms.BooleanField(
        label=_("Circular icon"),
        required=False,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField(
        choices=ICON_TAG_TYPES,
        initial=first_choice(ICON_TAG_TYPES),
    )
