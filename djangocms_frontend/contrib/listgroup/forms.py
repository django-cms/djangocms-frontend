from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings

from ...fields import AttributesFormField
from ...models import FrontendUIItem
from .constants import LISTGROUP_STATE_CHOICES


class ListGroupForm(EntangledModelForm):
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


class ListGroupItemForm(EntangledModelForm):
    """
    Components > "List Group Item" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "list_context",
                "list_state",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    list_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE,
        required=False,
    )
    list_state = forms.ChoiceField(
        label=_("State"),
        choices=LISTGROUP_STATE_CHOICES,
        initial=LISTGROUP_STATE_CHOICES[-1][0],
    )
    attributes = AttributesFormField()
