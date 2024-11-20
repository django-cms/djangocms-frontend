from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings

from ...common import MarginFormMixin, PaddingFormMixin, ResponsiveFormMixin
from ...fields import AttributesFormField, ButtonGroup, ColoredButtonGroup, TagTypeFormField
from ...models import FrontendUIItem
from .constants import LISTGROUP_STATE_CHOICES


class ListGroupForm(MarginFormMixin, ResponsiveFormMixin, EntangledModelForm):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "list_group_flush",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    list_group_flush = forms.BooleanField(
        label=_("List group flush"),
        initial=False,
        required=False,
        help_text=_("Create lists of content in a card with a flush list group."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class ListGroupItemForm(PaddingFormMixin, ResponsiveFormMixin, EntangledModelForm):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "simple_content",
                "list_context",
                "list_state",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    simple_content = forms.CharField(
        label=_("One line content"),
        required=False,
        help_text=_("List item text. Is only show if this list item has no child plugins."),
    )
    list_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ColoredButtonGroup(),
    )
    list_state = forms.ChoiceField(
        label=_("State"),
        choices=settings.EMPTY_CHOICE + LISTGROUP_STATE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ButtonGroup(attrs=dict(property="list_state")),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
