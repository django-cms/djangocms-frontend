from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from ...models import FrontendUIItem

# TODO leaving this comment for now
# data-bs-toggle="collapse" data-bs-target="#collapseExample"
# aria-expanded="false" aria-controls="collapseExample">
# data-bs-target can also be classes
# data-bs-parent links to the wrapper collapse
# <div class="collapse" id="collapseExample">


class CollapseForm(EntangledModelForm):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "collapse_siblings",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    collapse_siblings = forms.CharField(
        label=_("Siblings"),
        initial=".card",
        required=False,
        help_text=_("Element to be used to create accordions."),
    )


class CollapseTriggerForm(EntangledModelForm):
    """
    Component > "Collapse Trigger" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "trigger_identifier",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    trigger_identifier = forms.SlugField(
        label=_("Unique identifier"),
        required=True,
        help_text=_("Identifier to connect trigger with container."),
    )


class CollapseContainerForm(EntangledModelForm):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "container_identifier",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    container_identifier = forms.SlugField(
        label=_("Unique identifier"),
        required=True,
        help_text=_("Identifier to connect trigger with container."),
    )
