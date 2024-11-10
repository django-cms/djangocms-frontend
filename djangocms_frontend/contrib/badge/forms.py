from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField, ColoredButtonGroup, TagTypeFormField
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES


class BadgeForm(EntangledModelForm):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "badge_text",
                "badge_context",
                "badge_pills",
                "attributes",
            ]
        }

    badge_text = forms.CharField(
        label=_("Badge text"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "js-prepopulate-selected-text"}),
    )
    badge_context = forms.ChoiceField(
        label=_("Context"),
        choices=COLOR_STYLE_CHOICES,
        initial=first_choice(COLOR_STYLE_CHOICES),
        widget=ColoredButtonGroup(),
    )
    badge_pills = forms.BooleanField(
        label=_("Pills style"),
        initial=False,
        required=False,
        help_text=_("Activates the pills style."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
