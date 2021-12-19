from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import COLOR_STYLE_CHOICES

from ...models import FrontendUIItem


class AlertForm(EntangledModelForm):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "alert_context",
                "alert_dismissable",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    alert_context = forms.ChoiceField(
        label=_("Context"),
        choices=COLOR_STYLE_CHOICES,
        initial=COLOR_STYLE_CHOICES[0][0],
    )
    alert_dismissable = forms.BooleanField(
        label=_("Dismissable"),
        initial=False,
        required=False,
        help_text=_("Allows the alert to be closed."),
    )
