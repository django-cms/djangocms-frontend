from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...fields import AttributesFormField
from ...models import FrontendUIItem
from .constants import (
    TAB_ALIGNMENT_CHOICES,
    TAB_EFFECT_CHOICES,
    TAB_TEMPLATE_CHOICES,
    TAB_TYPE_CHOICES,
)


class TabForm(EntangledModelForm):
    """
    Components > "Navs - Tab" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "tab_type",
                "tab_alignment",
                "tab_index",
                "tab_effect",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Template"),
        choices=TAB_TEMPLATE_CHOICES,
        initial=TAB_TEMPLATE_CHOICES[0][0],
        help_text=_("This is the template that will be used for the component."),
    )
    tab_type = forms.ChoiceField(
        label=_("Type"),
        choices=TAB_TYPE_CHOICES,
        initial=TAB_TYPE_CHOICES[0][0],
    )
    tab_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=TAB_ALIGNMENT_CHOICES,
        required=False,
    )
    tab_index = forms.IntegerField(
        label=_("Index"),
        min_value=1,
        required=False,
        help_text=_("Index of element to open on page load starting at 1."),
    )
    tab_effect = forms.ChoiceField(
        label=_("Animation effect"),
        choices=settings.EMPTY_CHOICE + TAB_EFFECT_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()


class TabItemForm(EntangledModelForm):
    """
    Components > "Navs - Tab Item" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "tab_title",
                "tab_bordered",
                "tab_padding_size",
                "tab_padding_side",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    tab_title = forms.CharField(
        label=_("Tab title"),
    )
    tab_bordered = forms.BooleanField(
        label=_("Bordered"),
        required=False,
        help_text=_("Add borders to the tab item"),
    )
    tab_padding_size = forms.ChoiceField(
        label=_("Internal padding size"),
        choices=settings.SPACER_SIZE_CHOICES,
        initial=settings.SPACER_SIZE_CHOICES[1][0],
    )
    tab_padding_side = forms.ChoiceField(
        label=_("Internal padding sides"),
        choices=settings.SPACER_SIDE_CHOICES,
        initial=settings.SPACER_SIDE_CHOICES[0][0],
        required=False,
    )

    attributes = AttributesFormField()
