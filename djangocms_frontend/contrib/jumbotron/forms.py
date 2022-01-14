from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField


class JumbotronForm(EntangledModelForm):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_("Adds the .jumbotron-fluid class."),
    )
    attributes = AttributesFormField()
