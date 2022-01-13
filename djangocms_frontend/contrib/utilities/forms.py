from django import forms
from django.utils.translation import gettext as _
from djangocms_attributes_field.fields import AttributesFormField, AttributesWidget
from entangled.forms import EntangledModelForm

from ... import settings
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


class HeadingForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "heading_level",
                "heading",
                "heading_id",
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


class TableOfContentsForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": ["list_attributes", "link_attributes"],
        }
        untangled_fields = ("attributes",)
        help_texts = {
            "attributes": _(
                "Attributes apply to the <b>list items</b> for each entry in the table of contents."
            ),
        }
        labels = {
            "attributes": _("Item attributes"),
        }

    list_attributes = AttributesFormField(
        label=_("List attributes"),
        widget=AttributesWidget(),
        required=False,
        help_text=_(
            "Attributes apply to the <b>list</b> for each level in the table of contents."
        ),
    )

    link_attributes = AttributesFormField(
        label=_("Link attributes"),
        widget=AttributesWidget(),
        required=False,
        help_text=_(
            "Attributes apply to the <b>link</b> for each entry in the table of contents."
        ),
    )
