from django import forms
from django.conf import settings as django_settings
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from djangocms_picture.backends import BasePictureBackend
from djangocms_picture.models import RenditionPreset
from filer.models import ThumbnailOption

from djangocms_frontend import settings

from ...common import MarginFormMixin, ResponsiveFormMixin
from ...fields import AttributesFormField, TagTypeFormField, TemplateChoiceMixin
from ...helpers import first_choice
from ...models import FrontendUIItem
from ..link.forms import AbstractLinkForm
from .fields import ImageFormField, get_picture_reference


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
                "lazy_loading",
                "width",
                "height",
                "alignment",
                "link_attributes",
                "use_crop",
                "use_upscale",
                "use_responsive_image",
                "thumbnail_options",
                "rendition_preset",
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
    # Replaced by a request-aware ImageFormField in __init__. Keeping a
    # declared field makes it visible to django CMS's fieldset processing.
    picture = forms.Field(label=_("Image source"), required=False)
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
    rendition_preset = forms.ModelChoiceField(
        queryset=RenditionPreset.objects.all(),
        label=_("Rendition preset"),
        required=False,
        help_text=_("Portable rendition settings for image sources other than django-filer."),
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

    def __init__(
        self,
        *args,
        request: HttpRequest | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        source_field = ImageFormField(
            request=request,
            label=_("Image source"),
            required=False,
        )
        self.fields["picture"] = source_field

        reference = get_picture_reference(
            self.instance.config,
            "picture",
            external_field_name="external_picture",
        )
        selected_backend = self._get_selected_backend(reference)
        if not self.is_bound and reference:
            self.initial["picture"] = source_field.selection_from_reference(reference)
        self._configure_backend_fields(selected_backend)

    def _get_selected_backend(self, reference) -> BasePictureBackend:
        alias = self.data.get(f"{self.add_prefix('picture')}_backend") if self.is_bound else None
        alias = alias or (reference.backend if reference else None)
        alias = alias or getattr(django_settings, "DJANGOCMS_PICTURE_DEFAULT_BACKEND", "filer")
        return self.fields["picture"].backends_by_alias.get(alias, self.fields["picture"].backends[0])

    def _configure_backend_fields(self, backend: BasePictureBackend) -> None:
        for field_name in (
            "use_crop",
            "use_upscale",
            "use_responsive_image",
            "thumbnail_options",
            "rendition_preset",
        ):
            field = self.fields[field_name]
            field.disabled = not backend.supports_configuration_field(field_name)
            field.widget.attrs["data-picture-backend-option"] = field_name

    def clean(self):
        super().clean()
        data = self.cleaned_data
        if not data.get("picture", False):
            raise forms.ValidationError(_("You need to select an image source."))

        # certain cropping options do not work together, the following
        # list defines the disallowed options used in the ``clean`` method
        invalid_option_pairs = [
            ("thumbnail_options", "use_crop"),
            ("thumbnail_options", "use_upscale"),
            ("rendition_preset", "use_crop"),
            ("rendition_preset", "use_upscale"),
        ]
        # invalid_option_pairs
        invalid_option_pair = None

        for pair in invalid_option_pairs:
            if (
                not self.fields[pair[0]].disabled
                and not self.fields[pair[1]].disabled
                and data.get(pair[0], False)
                and data.get(pair[1], False)
            ):
                invalid_option_pair = pair
                break

        if invalid_option_pair:
            message = _('Invalid cropping settings. You cannot combine "{field_a}" with "{field_b}".')
            message = message.format(
                field_a=self.fields[invalid_option_pair[0]].label,
                field_b=self.fields[invalid_option_pair[1]].label,
            )
            raise forms.ValidationError(message)
        return data

    def _clean_form(self):
        super()._clean_form()
        config = self.cleaned_data.get("config")
        if config is not None:
            # Old URL values are converted to the URL backend on a successful edit.
            config.pop("external_picture", None)
