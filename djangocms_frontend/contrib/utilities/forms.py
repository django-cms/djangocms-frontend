from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from ... import settings
from ...fields import AttributesFormField
from ...models import FrontendUIItem


class SpacingForm(EntangledModelForm):
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
        initial=settings.SPACER_PROPERTY_CHOICES[0][0],
    )
    space_sides = forms.ChoiceField(
        label=_("Sides"),
        choices=settings.SPACER_SIDE_CHOICES,
        initial=settings.SPACER_SIDE_CHOICES[0][0],
        required=False,
    )
    space_size = forms.ChoiceField(
        label=_("Size"),
        choices=settings.SPACER_SIZE_CHOICES,
        initial=settings.SPACER_SIZE_CHOICES[0][0],
    )
    space_device = forms.ChoiceField(
        label=_("Device"),
        choices=settings.EMPTY_CHOICE + settings.DEVICE_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()


class HeadingForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "heading_level",
                "heading",
                "heading_id",
                "attributes",
            ],
        }
        untangled_fields = ("attributes",)

    HEADINGS = (
        ("h1", _("Heading 1")),
        ("h2", _("Heading 2")),
        ("h3", _("Heading 3")),
        ("h4", _("Heading 4")),
        ("h5", _("Heading 5")),
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
        help_text=_(
            "Fill in unique ID for table of contents. If empty heading will not appear in table of contents."
        ),
    )
    attributes = AttributesFormField()


class TableOfContentsForm(EntangledModelForm):
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
        help_text=_(
            "Attributes apply to the <b>list</b> for each level in the table of contents."
        ),
    )

    link_attributes = AttributesFormField(
        label=_("Link attributes"),
        help_text=_(
            "Attributes apply to the <b>link</b> for each entry in the table of contents."
        ),
    )
    attributes = AttributesFormField(
        label=_("Item attributes"),
        help_text=_(
            "Attributes apply to the <b>list items</b> for each entry in the table of contents."
        ),
    )
