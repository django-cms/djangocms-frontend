from django import forms
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminImageFormField, FilerImageField
from filer.models import Image, ThumbnailOption

from djangocms_frontend import settings

from ...fields import AttributesFormField
from ...models import FrontendUIItem
from ..link.forms import AbstractLinkForm

#
# def get_model_form_fields(form, exclude):
#     plugin_fields = ("cmsplugin_ptr",)
#     return [
#         field.name
#         for field in form._meta.get_fields(include_parents=False)
#         if field.name not in plugin_fields and field.name not in exclude
#     ]
#
#
# abstract_picture_fields = get_model_form_fields(
#     AbstractPicture, ("image", "link_page", "tag_type", "attributes")
# )
#
#
# class PictureFormMetaClass(EntangledFormMetaclass):
#     def __new__(cls, class_name, bases, attrs):
#         for field in abstract_picture_fields:
#             model_field = AbstractPicture._meta.get_field(field)
#             if field not in attrs:
#                 attrs[field] = model_field.formfield()
#         return super().__new__(cls, class_name, bases, attrs)
#


def get_alignment():
    """add setting for image alignment, renders a class or inline styles depending on your template setup"""
    alignment = getattr(
        settings,
        "DJANGOCMS_PICTURE_ALIGN",
        (
            ("start", _("Align left")),
            ("end", _("Align right")),
            ("center", _("Align center")),
        ),
    )
    return alignment


def get_templates():
    """Add additional choices through the ``settings.py``."""
    choices = [
        ("default", _("Default")),
    ]
    choices += getattr(
        settings,
        "DJANGOCMS_PICTURE_TEMPLATES",
        [],
    )
    return choices


# required for backwards compability
PICTURE_ALIGNMENT = get_alignment()


LINK_TARGET = (
    ("_blank", _("Open in new window")),
    ("_self", _("Open in same window")),
    ("_parent", _("Delegate to parent")),
    ("_top", _("Delegate to top")),
)

RESPONSIVE_IMAGE_CHOICES = (
    ("inherit", _("Let settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES decide")),
    ("yes", _("Yes")),
    ("no", _("No")),
)


class ImageForm(AbstractLinkForm, EntangledModelForm):
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
                "width",
                "height",
                "alignment",
                "caption_text",
                "link_attributes",
                "use_automatic_scaling",
                "use_crop",
                "use_no_cropping",
                "use_upscale",
                "use_responsive_image",
                "thumbnail_options",
                "picture_fluid",
                "picture_rounded",
                "picture_thumbnail",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    link_is_optional = True

    template = forms.ChoiceField(
        label=_("Template"),
        choices=get_templates(),
        initial=get_templates()[0][0],
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
    width = forms.IntegerField(
        label=_("Width"),
        required=False,
        min_value=1,
        help_text=_(
            "The image width as number in pixels. " 'Example: "720" and not "720px".'
        ),
    )
    height = forms.IntegerField(
        label=_("Height"),
        required=False,
        min_value=1,
        help_text=_(
            "The image height as number in pixels. " 'Example: "720" and not "720px".'
        ),
    )
    alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=get_alignment(),
        required=False,
        help_text=_("Aligns the image according to the selected option."),
    )
    caption_text = forms.CharField(
        label=_("Caption text"),
        required=False,
        widget=forms.Textarea(attrs=dict(rows=2)),
        help_text=_(
            "Provide a description, attribution, copyright or other information."
        ),
    )
    link_attributes = AttributesFormField(
        label=_("Link attributes"),
        help_text=_("Attributes apply to the <b>link</b>."),
    )

    # cropping models
    # active per default
    use_automatic_scaling = forms.BooleanField(
        label=_("Automatic scaling"),
        required=False,
        help_text=_(
            "Uses the placeholder dimensions to automatically calculate the size."
        ),
    )
    # ignores all other cropping options
    # throws validation error if other cropping options are selected
    use_no_cropping = forms.BooleanField(
        label=_("Use original image"),
        required=False,
        help_text=_("Outputs the raw image without cropping."),
    )
    # upscale and crop work together
    # throws validation error if other cropping options are selected
    use_crop = forms.BooleanField(
        label=_("Crop image"),
        required=False,
        help_text=_(
            "Crops the image according to the thumbnail settings provided in the template."
        ),
    )
    use_upscale = forms.BooleanField(
        label=_("Upscale image"),
        required=False,
        help_text=_(
            "Upscales the image to the size of the thumbnail settings in the template."
        ),
    )
    use_responsive_image = forms.ChoiceField(
        label=_("Use responsive image"),
        choices=RESPONSIVE_IMAGE_CHOICES,
        initial=RESPONSIVE_IMAGE_CHOICES[0][0],
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
        help_text=_(
            "Overrides width, height, and crop; scales up to the provided preset dimensions."
        ),
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

    def clean(self):
        data = self.cleaned_data
        # there can be only one link type
        if (
            sum(
                (
                    bool(data["external_link"]),
                    bool(data["internal_link"]),
                    bool(data["file_link"]),
                )
            )
            > 1
        ):
            raise forms.ValidationError(
                _(
                    "You have given more than one external, internal, or file link target. "
                    "Only one option is allowed."
                )
            )

        # you shall only set one image kind
        if not data["picture"] and not data["external_picture"]:
            raise forms.ValidationError(
                _(
                    "You need to add either an image, "
                    "or a URL linking to an external image."
                )
            )

        # certain cropping options do not work together, the following
        # list defines the disallowed options used in the ``clean`` method
        invalid_option_pairs = [
            ("use_automatic_scaling", "use_no_cropping"),
            ("use_automatic_scaling", "thumbnail_options"),
            ("use_no_cropping", "use_crop"),
            ("use_no_cropping", "use_upscale"),
            ("use_no_cropping", "thumbnail_options"),
            ("thumbnail_options", "use_crop"),
            ("thumbnail_options", "use_upscale"),
        ]
        # invalid_option_pairs
        invalid_option_pair = None

        for pair in invalid_option_pairs:
            if data.get(pair[0]) and data.get(pair[1]):
                invalid_option_pair = pair
                break

        if invalid_option_pair:
            message = _(
                "Invalid cropping settings. "
                'You cannot combine "{field_a}" with "{field_b}".'
            )
            message = message.format(
                field_a=self.fields[invalid_option_pair[0]].label,
                field_b=self.fields[invalid_option_pair[0]].label,
            )
            raise forms.ValidationError(message)
