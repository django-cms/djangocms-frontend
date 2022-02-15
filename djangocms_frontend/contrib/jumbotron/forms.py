from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.contrib import jumbotron
from djangocms_frontend.fields import (
    AttributesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)

mixin_factory = settings.get_forms(jumbotron)


class JumbotronForm(mixin_factory("Jumbotron"), EntangledModelForm):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
                "jumbotron_context",
                "template",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Template"),
        choices=settings.JUMBOTRON_TEMPLATE_CHOICES,
        initial=settings.JUMBOTRON_TEMPLATE_CHOICES[0][0],
    )
    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_(
            "Makes the jumbotron full the will width of the container or window."
        ),
    )
    jumbotron_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ColoredButtonGroup(attrs=dict(property="color")),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
