from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...common import PaddingFormMixin
from ...fields import AttributesFormField, ButtonGroup, IconGroup, TagTypeFormField, TemplateChoiceMixin
from ...helpers import first_choice
from ...models import FrontendUIItem
from .constants import TAB_ALIGNMENT_CHOICES, TAB_EFFECT_CHOICES, TAB_TEMPLATE_CHOICES, TAB_TYPE_CHOICES


class TabForm(TemplateChoiceMixin, EntangledModelForm):
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
        label=_("Layout"),
        choices=TAB_TEMPLATE_CHOICES,
        initial=first_choice(TAB_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    tab_type = forms.ChoiceField(
        label=_("Type"),
        choices=TAB_TYPE_CHOICES,
        initial=first_choice(TAB_TYPE_CHOICES),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    tab_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + TAB_ALIGNMENT_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
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
    tag_type = TagTypeFormField()


class TabItemForm(PaddingFormMixin, EntangledModelForm):
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
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    tab_title = forms.CharField(
        label=_("Tab title"),
        initial=_("New tab"),
        required=True,
    )
    tab_bordered = forms.BooleanField(
        label=_("Bordered"),
        required=False,
        help_text=_("Add borders to the tab item"),
    )

    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
