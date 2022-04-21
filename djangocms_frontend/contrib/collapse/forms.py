from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...fields import AttributesFormField, TagTypeFormField
from ...models import FrontendUIItem
from .. import collapse

# TODO leaving this comment for now
# data-bs-toggle="collapse" data-bs-target="#collapseExample"
# aria-expanded="false" aria-controls="collapseExample">
# data-bs-target can also be classes
# data-bs-parent links to the wrapper collapse
# <div class="collapse" id="collapseExample">

mixin_factory = settings.get_forms(collapse)


class CollapseForm(mixin_factory("Collapse"), EntangledModelForm):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "collapse_siblings",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    collapse_siblings = forms.CharField(
        label=_("Siblings"),
        initial=".card",
        required=False,
        help_text=_("Element to be used to create accordions."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class CollapseTriggerForm(mixin_factory("CollapseTrigger"), EntangledModelForm):
    """
    Component > "Collapse Trigger" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "trigger_identifier",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    trigger_identifier = forms.SlugField(
        label=_("Unique identifier"),
        required=True,
        help_text=_("Identifier to connect trigger with container."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class CollapseContainerForm(mixin_factory("CollapseContainer"), EntangledModelForm):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "container_identifier",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    container_identifier = forms.SlugField(
        label=_("Unique identifier"),
        required=True,
        help_text=_("Identifier to connect trigger with container."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
