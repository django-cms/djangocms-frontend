from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...fields import AttributesFormField, ButtonGroup, TagTypeFormField
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import modal
from .constants import (
    MODAL_CENTERED_CHOICES,
    MODAL_FULLSCREEN_CHOICES,
    MODAL_INNER_TYPE_CHOICES,
    MODAL_SIZE_CHOICES,
)

# TODO leaving this comment for now
# data-bs-toggle="modal" data-bs-target="#modalExample"
# aria-expanded="false" aria-controls="modalExample">
# data-bs-target can also be classes
# data-bs-parent links to the wrapper modal
# <div class="modal" id="modalExample">

mixin_factory = settings.get_forms(modal)


class ModalForm(mixin_factory("Modal"), EntangledModelForm):
    """
    Component > "Modal" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "modal_siblings",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    modal_siblings = forms.CharField(
        label=_("Siblings"),
        initial=".card",
        required=False,
        help_text=_("Element to be used to create a modal."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class ModalTriggerForm(mixin_factory("ModalTrigger"), EntangledModelForm):
    """
    Component > "Modal Trigger" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
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


class ModalContainerForm(mixin_factory("ModalContainer"), EntangledModelForm):
    """
    Component > "Modal Container" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "container_identifier",
                "attributes",
                "modal_centered",
                "modal_static",
                "modal_scrollable",
                "modal_size",
                "modal_fullscreen",
            ]
        }
        untangled_fields = ("tag_type",)

    container_identifier = forms.SlugField(
        label=_("Unique identifier"),
        required=True,
        help_text=_("Identifier to connect trigger with container."),
    )

    modal_centered = forms.ChoiceField(
        label=_("Centered"),
        choices=settings.EMPTY_CHOICE + MODAL_CENTERED_CHOICES,
        required=False,
    )

    modal_static = forms.BooleanField(
        label=_("Static backdrop"),
        required=False,
        help_text=_("Disable scrolling in the container."),
    )

    modal_scrollable = forms.BooleanField(
        label=_("Scrollable"),
        required=False,
        help_text=_("Enable scrolling in the container."),
    )

    modal_size = forms.ChoiceField(
        label=_("Size"),
        choices=settings.EMPTY_CHOICE + MODAL_SIZE_CHOICES,
        required=False,
    )

    modal_fullscreen = forms.ChoiceField(
        label=_("Fullscreen"),
        choices=settings.EMPTY_CHOICE + MODAL_FULLSCREEN_CHOICES,
        required=False,
    )

    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class ModalInnerForm(mixin_factory("ModalInner"), EntangledModelForm):
    """
    Component > "Modal Container Content" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "inner_type",
            ]
        }
        untangled_fields = ("tag_type",)

    inner_type = forms.ChoiceField(
        label=_("Type"),
        choices=settings.EMPTY_CHOICE + MODAL_INNER_TYPE_CHOICES,
        required=True,
    )

    inner_type = forms.ChoiceField(
        label=_("Inner type"),
        choices=MODAL_INNER_TYPE_CHOICES,
        initial=first_choice(MODAL_INNER_TYPE_CHOICES),
        help_text=_("Define the structure of the plugin."),
        widget=ButtonGroup(attrs=dict(label_class="btn-secondary")),
    )
    attributes = AttributesFormField()
