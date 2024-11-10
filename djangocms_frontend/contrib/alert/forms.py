from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common import ResponsiveFormMixin, SpacingFormMixin
from djangocms_frontend.contrib import alert
from djangocms_frontend.fields import AttributesFormField, ColoredButtonGroup, TagTypeFormField
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES

mixin_factory = settings.get_forms(alert)


class AlertForm(mixin_factory("Alert"), ResponsiveFormMixin, SpacingFormMixin, EntangledModelForm):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "alert_context",
                "alert_dismissible",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    alert_context = forms.ChoiceField(
        label=_("Context"),
        choices=COLOR_STYLE_CHOICES,
        initial=first_choice(COLOR_STYLE_CHOICES),
        widget=ColoredButtonGroup(),
    )
    alert_dismissible = forms.BooleanField(
        label=_("Dismissible"),
        initial=False,
        required=False,
        help_text=_("Allows the alert to be closed."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
