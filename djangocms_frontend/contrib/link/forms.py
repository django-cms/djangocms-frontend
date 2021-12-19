from cms.models import Page
from django import forms
from django.utils.translation import gettext as _
from djangocms_icon.fields import IconField
from djangocms_link.models import TARGET_CHOICES
from djangocms_link.validators import IntranetURLValidator
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminImageFormField
from filer.models import Image

from djangocms_frontend.settings import COLOR_STYLE_CHOICES

from ... import settings
from ...models import FrontendUIItem
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES


def get_templates():
    choices = [
        ("default", _("Default")),
    ]
    choices += getattr(
        settings,
        "DJANGOCMS_LINK_TEMPLATES",
        [],
    )
    return choices


HOSTNAME = getattr(settings, "DJANGOCMS_LINK_INTRANET_HOSTNAME_PATTERN", None)


class AbstractLinkForm(EntangledModelForm):
    abstract_entangled_fields = [
        "template",
        "name",
        "external_link",
        "internal_link",
        "file_link",
        "anchor",
        "mailto",
        "phone",
        "target",
    ]
    url_validators = [
        IntranetURLValidator(intranet_host_re=HOSTNAME),
    ]

    template = forms.ChoiceField(
        label=_("Template"),
        choices=get_templates(),
        initial=get_templates()[0][0],
    )
    name = forms.CharField(
        label=_("Display name"),
        required=False,
    )
    external_link = forms.CharField(
        label=_("External link"),
        required=False,
        validators=url_validators,
        help_text=_("Provide a link to an external source."),
    )
    internal_link = forms.ModelChoiceField(
        queryset=None,
        to_field_name="title",
        label=_("Internal link"),
        required=False,
        help_text=_("If provided, overrides the external link."),
    )
    file_link = AdminImageFormField(
        rel=Image,
        queryset=Image.objects.all(),
        to_field_name="id",
        label=_("File link"),
        required=False,
        help_text=_("If provided links a file from the filer app."),
    )
    # other link types
    anchor = forms.CharField(
        label=_("Anchor"),
        required=False,
        help_text=_(
            "Appends the value only after the internal or external link. "
            'Do <em>not</em> include a preceding "#" symbol.'
        ),
    )
    mailto = forms.EmailField(
        label=_("Email address"),
        required=False,
    )
    phone = forms.CharField(
        label=_("Phone"),
        required=False,
    )
    # advanced options
    target = forms.ChoiceField(
        label=_("Target"),
        choices=settings.EMPTY_CHOICE + TARGET_CHOICES,
        required=False,
    )


class LinkForm(AbstractLinkForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": AbstractLinkForm.abstract_entangled_fields
            + [
                "link_type",
                "link_context",
                "link_size",
                "link_outline",
                "link_block",
                "icon_left",
                "icon_right",
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    link_type = forms.ChoiceField(
        label=_("Type"),
        choices=LINK_CHOICES,
        initial=LINK_CHOICES[0][0],
        widget=forms.RadioSelect(attrs={"class": "inline-block"}),
        help_text=_("Adds either the .btn-* or .text-* classes."),
    )
    link_context = forms.ChoiceField(
        label=_("Context"), choices=COLOR_STYLE_CHOICES, required=False
    )
    link_size = forms.ChoiceField(
        label=_("Size"),
        choices=settings.EMPTY_CHOICE + LINK_SIZE_CHOICES,
        required=False,
    )
    link_outline = forms.BooleanField(
        label=_("Outline"),
        initial=False,
        required=False,
        help_text=_("Applies the .btn-outline class to the elements."),
    )
    link_block = forms.BooleanField(
        label=_("Block"),
        initial=False,
        required=False,
        help_text=_("Extends the button to the width of its container."),
    )
    icon_left = IconField(
        label=_("Icon left"),
        required=False,
    )
    icon_right = IconField(
        label=_("Icon right"),
        required=False,
    )
