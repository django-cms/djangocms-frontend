from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common import BackgroundFormMixin, ResponsiveFormMixin, SpacingFormMixin
from djangocms_frontend.contrib import jumbotron
from djangocms_frontend.contrib.jumbotron import models
from djangocms_frontend.fields import AttributesFormField, TagTypeFormField, TemplateChoiceMixin
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
        model = models.Jumbotron
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
                "template",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=settings.JUMBOTRON_TEMPLATE_CHOICES,
        initial=first_choice(settings.JUMBOTRON_TEMPLATE_CHOICES),
    )
    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_("Makes the jumbotron fill the full width of the container or window."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
