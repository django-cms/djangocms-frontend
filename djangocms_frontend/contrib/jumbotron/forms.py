from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.responsive import ResponsiveFormMixin
from djangocms_frontend.common.spacing import SpacingFormMixin
from djangocms_frontend.contrib import jumbotron
from djangocms_frontend.fields import (
    AttributesFormField,
    TagTypeFormField,
    TemplateChoiceMixin,
)
from djangocms_frontend.helpers import first_choice

mixin_factory = settings.get_forms(jumbotron)


class JumbotronForm(
    mixin_factory("Jumbotron"),
    ResponsiveFormMixin,
    SpacingFormMixin,
    BackgroundFormMixin,
    TemplateChoiceMixin,
    EntangledModelForm,
):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
                "template",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Template"),
        choices=settings.JUMBOTRON_TEMPLATE_CHOICES,
        initial=first_choice(settings.JUMBOTRON_TEMPLATE_CHOICES),
    )
    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_(
            "Makes the jumbotron fill the full width of the container or window."
        ),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
