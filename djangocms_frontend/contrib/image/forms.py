from django import forms
from django.conf import settings as django_settings
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from filer.fields.image import AdminImageFormField, FilerImageField
from filer.models import Image, ThumbnailOption

from djangocms_frontend import settings

from ...common import MarginFormMixin, ResponsiveFormMixin
from ...fields import AttributesFormField, TagTypeFormField, TemplateChoiceMixin
from ...helpers import first_choice
from ...models import FrontendUIItem
from ..link.forms import AbstractLinkForm


def get_alignment():
    """add setting for image alignment, renders a class or inline styles depending on your template setup"""
    alignment = getattr(
        settings,
        "DJANGOCMS_PICTURE_ALIGN",
        (
            ("start", _("Float left")),
            ("end", _("Float right")),
            ("center", _("Align center")),
        ),
    )
    return alignment


def get_templates():
    """Add additional choices through the ``settings.py``."""
    choices = getattr(
        django_settings,
        "DJANGOCMS_PICTURE_TEMPLATES",
        [
            ("default", _("Default")),
        ],
    )
    return choices


# required for backwards compatibility
PICTURE_ALIGNMENT = get_alignment()


RESPONSIVE_IMAGE_CHOICES = (
    ("inherit", _("Let settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES decide")),
    ("yes", _("Yes")),
    ("no", _("No")),
)


class ImageForm(
    TemplateChoiceMixin,
    ResponsiveFormMixin,
    MarginFormMixin,
    AbstractLinkForm,
):
    """
    Content > "Image" Plugin
    https://getbootstrap.com/docs/5.0/content/images/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "picture",
                "external_picture",
                "lazy_loading",
                "width",
                "height",
                "alignment",
                "link_attributes",
                "use_crop",
                "use_upscale",
                "use_responsive_image",
                "thumbnail_options",
                "picture_fluid",
                "picture_rounded",
                "picture_thumbnail",
                "attributes",
            ]
        }
        exclude = ("ui_item",)

    link_is_optional = True

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=get_templates(),
        initial=first_choice(get_templates()),
    )
    picture = AdminImageFormField(
        rel=ManyToOneRel(FilerImageField, Image, "id"),
        queryset=Image.objects.all(),
        to_field_name="id",
        label=_("Image"),
        required=False,
    )
    external_picture = forms.URLField(
        label=_("External image"),
        required=False,
        help_text=_(
            "If provided, overrides the embedded image. "
            "Certain options such as cropping are not applicable to external images."
        ),
    )
    lazy_loading = forms.BooleanField(
        label=_("Load lazily"),
        required=False,
        help_text=_("Use for images below the fold. This will load images only if user scrolls them into view. "),
    )

    width = forms.IntegerField(
        label=_("Width"),
        required=False,
        min_value=1,
        help_text=_('The image width as number in pixels (eg, "720" and not "720px"). '),
    )
    height = forms.IntegerField(
        label=_("Height"),
        required=False,
        min_value=1,
        help_text=_(
            'The image height as number in pixels (eg, "720" and not "720px"). '
            "Note: if width is set, height will be calculated automatically to preserve aspect ratio. "
            "In case of cropping, then both width and height are applied as given."
        ),
    )
    alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + get_alignment(),
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        help_text=_("Aligns the image according to the selected option."),
    )
    link_attributes = AttributesFormField(
        label=_("Link attributes"),
        help_text=_("Attributes apply to the <b>link</b>."),
    )

    # upscale and crop work together
    # throws validation error if other cropping options are selected
    use_crop = forms.BooleanField(
        label=_("Crop image"),
        required=False,
        help_text=_("Crops the image rather than resizing"),
    )
    use_upscale = forms.BooleanField(
        label=_("Upscale image"),
        required=False,
        help_text=_("Allows the image to be upscaled beyond its original size."),
    )
    use_responsive_image = forms.ChoiceField(
        label=_("Use responsive image"),
        choices=RESPONSIVE_IMAGE_CHOICES,
        initial=first_choice(RESPONSIVE_IMAGE_CHOICES),
        help_text=_(
            "Uses responsive image technique to choose better image to display based upon screen viewport. "
            "This configuration only applies to uploaded images (external pictures will not be affected). "
        ),
    )
    # overrides all other options
    # throws validation error if other cropping options are selected
    thumbnail_options = forms.ModelChoiceField(
        queryset=ThumbnailOption.objects.all(),
        to_field_name="id",
        label=_("Thumbnail options"),
        required=False,
        help_text=_("Overrides width, height, and crop; scales up to the provided preset dimensions."),
    )
    picture_fluid = forms.BooleanField(
        label=_("Responsive"),
        required=False,
        initial=True,
        help_text=_("Adds the .img-fluid class to make the image responsive."),
    )
    picture_rounded = forms.BooleanField(
        label=_("Rounded"),
        required=False,
        initial=False,
        help_text=_("Adds the .rounded class for round corners."),
    )
    picture_thumbnail = forms.BooleanField(
        label=_("Thumbnail"),
        required=False,
        initial=False,
        help_text=_("Adds the .img-thumbnail class."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

    def clean(self):
        super().clean()
        data = self.cleaned_data
        # you shall only set one image kind
        if not data.get("picture", False) and not data.get("external_picture", False):
            raise forms.ValidationError(_("You need to add either an image, or a URL linking to an external image."))

        # certain cropping options do not work together, the following
        # list defines the disallowed options used in the ``clean`` method
        invalid_option_pairs = [
            ("thumbnail_options", "use_crop"),
            ("thumbnail_options", "use_upscale"),
        ]
        # invalid_option_pairs
        invalid_option_pair = None

        for pair in invalid_option_pairs:
            if data.get(pair[0], False) and data.get(pair[1], False):
                invalid_option_pair = pair
                break

        if invalid_option_pair:
            message = _('Invalid cropping settings. You cannot combine "{field_a}" with "{field_b}".')
            message = message.format(
                field_a=self.fields[invalid_option_pair[0]].label,
                field_b=self.fields[invalid_option_pair[0]].label,
            )
            raise forms.ValidationError(message)
