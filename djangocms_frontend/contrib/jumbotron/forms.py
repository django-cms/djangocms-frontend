from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm


class JumbotronForm(EntangledModelForm):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_fluid",
            ]
        }
        untangled_fields = (
            "tag_type",
            "attributes",
        )

    jumbotron_fluid = forms.BooleanField(
        label=_("Fluid"),
        initial=False,
        required=False,
        help_text=_("Adds the .jumbotron-fluid class."),
    )
