from django import forms
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminImageFormField, FilerImageField
from filer.models import Image

from djangocms_frontend.fields import AttributesFormField, ButtonGroup, TagTypeFormField, TemplateChoiceMixin

from ... import settings
from ...common import BackgroundFormMixin
from ...fields import HTMLFormField
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import carousel
from ..link.forms import LinkFormMixin
from .constants import (
    CAROUSEL_ASPECT_RATIO_CHOICES,
    CAROUSEL_PAUSE_CHOICES,
    CAROUSEL_TEMPLATE_CHOICES,
    CAROUSEL_TRANSITION_CHOICES,
)

mixin_factory = settings.get_forms(carousel)


class CarouselForm(mixin_factory("Carousel"), TemplateChoiceMixin, EntangledModelForm):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "carousel_aspect_ratio",
                "carousel_controls",
                "carousel_indicators",
                "carousel_interval",
                "carousel_keyboard",
                "carousel_pause",
                "carousel_ride",
                "carousel_wrap",
                "carousel_transition",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=CAROUSEL_TEMPLATE_CHOICES,
        initial=first_choice(CAROUSEL_TEMPLATE_CHOICES),
        help_text=_("This is the template that will be used for the component."),
    )
    carousel_interval = forms.IntegerField(
        label=_("Interval"),
        initial=5000,
        help_text=_(
            "The amount of time to delay between automatically cycling "
            "an item. If false, carousel will not automatically cycle."
        ),
    )
    carousel_controls = forms.BooleanField(
        label=_("Controls"),
        initial=True,
        required=False,
        help_text=_("Adding in the previous and next controls."),
    )
    carousel_indicators = forms.BooleanField(
        label=_("Indicators"),
        initial=True,
        required=False,
        help_text=_("Adding in the indicators to the carousel."),
    )
    carousel_keyboard = forms.BooleanField(
        label=_("Keyboard"),
        initial=True,
        required=False,
        help_text=_("Whether the carousel should react to keyboard events."),
    )
    carousel_pause = forms.ChoiceField(
        label=_("Pause"),
        choices=CAROUSEL_PAUSE_CHOICES,
        initial=first_choice(CAROUSEL_PAUSE_CHOICES),
        help_text=_(
            'If set to "hover", pauses the cycling of the carousel on '
            '"mouseenter" and resumes the cycling of the carousel on '
            '"mouseleave". If set to "false", hovering over the carousel '
            "won't pause it."
        ),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    carousel_ride = forms.BooleanField(
        label=_("Auto start"),
        initial=True,
        required=False,
        help_text=_(
            "Autoplays the carousel after the user manually cycles the "
            'first item. If "carousel", autoplays the carousel on load.'
        ),
    )
    carousel_wrap = forms.BooleanField(
        label=_("Wrap"),
        initial=True,
        required=False,
        help_text=_("Whether the carousel should cycle continuously or have hard stops."),
    )
    carousel_aspect_ratio = forms.ChoiceField(
        label=_("Aspect ratio"),
        choices=settings.EMPTY_CHOICE + CAROUSEL_ASPECT_RATIO_CHOICES,
        required=False,
        initial=settings.EMPTY_CHOICE[0][0],
        help_text=_("Determines width and height of the image according to the selected ratio."),
    )
    carousel_transition = forms.ChoiceField(
        label=_("Transition"),
        choices=CAROUSEL_TRANSITION_CHOICES,
        required=False,
        initial=CAROUSEL_TRANSITION_CHOICES[0][0],
        help_text=_("Determines if slides change by sliding or fading."),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    attributes = AttributesFormField(
        excluded_keys=[
            "id",
            "data-bs-interval",
            "data-bs-keyboard",
            "data-bs-pause",
            "data-bs-ride",
            "data-bs-wrap",
        ],
    )
    tag_type = TagTypeFormField()


class CarouselSlideForm(
    mixin_factory("CarouselSlide"),
    BackgroundFormMixin,
    LinkFormMixin,
    EntangledModelForm,
):
    """
    Components > "Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "carousel_image",
                "carousel_content",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    link_is_optional = True

    carousel_image = AdminImageFormField(
        rel=ManyToOneRel(FilerImageField, Image, "id"),
        queryset=Image.objects.all(),
        to_field_name="id",
        label=_("Slide image"),
        required=False,
    )
    carousel_content = HTMLFormField(
        label=_("Content"),
        required=False,
        initial="",
        help_text=_("Content may also be added using child plugins."),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
