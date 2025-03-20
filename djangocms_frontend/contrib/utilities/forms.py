from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...common import SpacingFormMixin
from ...fields import AttributesFormField, ButtonGroup, ColoredButtonGroup, IconGroup, TagTypeFormField
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import utilities

mixin_factory = settings.get_forms(utilities)


class SpacingForm(mixin_factory("Spacing"), EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "space_property",
                "space_sides",
                "space_size",
                "space_device",
                "attributes",
            ],
        }
        untangled_fields = ("tag_type",)

    space_property = forms.ChoiceField(
        label=_("Property"),
        choices=settings.SPACER_PROPERTY_CHOICES,
        initial=first_choice(settings.SPACER_PROPERTY_CHOICES),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    space_sides = forms.ChoiceField(
        label=_("Sides"),
        choices=settings.SPACER_SIDE_CHOICES,
        initial=first_choice(settings.SPACER_SIDE_CHOICES),
        required=False,
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    space_size = forms.ChoiceField(
        label=_("Size"),
        choices=settings.SPACER_SIZE_CHOICES + (("auto", _("Auto")),),
        initial=first_choice(settings.SPACER_SIZE_CHOICES),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    space_device = forms.ChoiceField(
        label=_("Device"),
        choices=settings.EMPTY_CHOICE + settings.DEVICE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

    def clean(self):
        super().clean()
        if self.cleaned_data["space_property"] == "p" and self.cleaned_data["space_size"] == "auto":
            raise ValidationError(
                {
                    "space_property": _(
                        "Padding does not have an auto spacing. Either switch to margin or a defined size."
                    ),
                    "space_size": _(
                        "Padding does not have an auto spacing. Either "
                        "switch to a defined size or change the spacing property."
                    ),
                }
            )


class HeadingForm(mixin_factory("Heading"), SpacingFormMixin, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "heading_level",
                "heading",
                "heading_id",
                "heading_context",
                "heading_alignment",
                "attributes",
            ],
        }
        untangled_fields = []

    HEADINGS = (
        ("h1", _("Heading 1")),
        ("h2", _("Heading 2")),
        ("h3", _("Heading 3")),
        ("h4", _("Heading 4")),
        ("h5", _("Heading 5")),
    )
    ALIGNMENT_CHOICES = (
        ("start", _("Left")),
        ("center", _("Center")),
        ("end", _("Right")),
    )

    heading_level = forms.ChoiceField(
        label=_("Heading level"),
        choices=getattr(settings, "DJANGO_FRONTEND_HEADINGS", HEADINGS),
        required=True,
    )

    heading = forms.CharField(
        label=_("Heading"),
        required=True,
    )

    heading_id = forms.CharField(
        label=_("ID"),
        required=False,
        help_text=_("Fill in unique ID for table of contents. If empty heading will not appear in table of contents."),
    )
    heading_context = forms.ChoiceField(
        label=_("Heading context"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE,
        widget=ColoredButtonGroup(),
    )
    heading_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + ALIGNMENT_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()


class TableOfContentsForm(mixin_factory("TableOfContents"), EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "list_attributes",
                "link_attributes",
                "attributes",
            ],
        }
        untangled_fields = ()

    list_attributes = AttributesFormField(
        label=_("List attributes"),
        help_text=_("Attributes apply to the <b>list</b> for each level in the table of contents."),
    )

    link_attributes = AttributesFormField(
        label=_("Link attributes"),
        help_text=_("Attributes apply to the <b>link</b> for each entry in the table of contents."),
    )
    attributes = AttributesFormField(
        label=_("Item attributes"),
        help_text=_("Attributes apply to the <b>list items</b> for each entry in the table of contents."),
    )
