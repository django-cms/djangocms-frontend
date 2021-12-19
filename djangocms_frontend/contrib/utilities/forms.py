from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...models import FrontendUIItem


class SpacingForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "space_property",
                "space_sides",
                "space_size",
                "space_device",
            ],
        }
        untangled_fields = ("tag_type",)

    space_property = forms.ChoiceField(
        label=_("Property"),
        choices=settings.SPACER_PROPERTY_CHOICES,
        initial=settings.SPACER_PROPERTY_CHOICES[0][0],
    )
    space_sides = forms.ChoiceField(
        label=_("Sides"),
        choices=settings.SPACER_SIDE_CHOICES,
        initial=settings.SPACER_SIDE_CHOICES[0][0],
    )
    space_size = forms.ChoiceField(
        label=_("Size"),
        choices=settings.SPACER_SIZE_CHOICES,
        initial=settings.SPACER_SIZE_CHOICES[0][0],
    )
    space_device = forms.ChoiceField(
        label=_("Device"),
        choices=settings.EMPTY_CHOICE + settings.DEVICE_CHOICES,
        required=False,
    )
