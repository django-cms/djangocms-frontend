from django import forms
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import ALIGN_CHOICES

from ... import settings
from ...common import BackgroundFormMixin, ResponsiveFormMixin, SpacingFormMixin
from ...fields import AttributesFormField, HTMLFormField, IconGroup, TagTypeFormField
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import content
from .constants import CODE_TYPE_CHOICES

mixin_factory = settings.get_forms(content)


class CodeForm(
    mixin_factory("Code"),
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    class Media:
        js = (
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in django_settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.js",
        )

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "code_content",
                "code_type",
                "attributes",
            ]
        }

    code_content = forms.CharField(
        label=_("Code"),
        initial="",
        required=True,
        widget=forms.widgets.Textarea(attrs={"class": "js-ckeditor-use-selected-text"}),
    )
    code_type = forms.ChoiceField(
        label=_("Code type"),
        choices=CODE_TYPE_CHOICES,
        initial=first_choice(CODE_TYPE_CHOICES),
        required=True,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class BlockquoteForm(
    mixin_factory("Blockquote"),
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "quote_content",
                "quote_origin",
                "quote_alignment",
                "attributes",
            ]
        }

    quote_content = HTMLFormField(
        label=_("Quote"),
        initial="",
        required=True,
    )
    quote_origin = HTMLFormField(
        label=_("Source"),
        required=False,
    )
    quote_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class FigureForm(
    mixin_factory("Figure"),
    SpacingFormMixin,
    ResponsiveFormMixin,
    BackgroundFormMixin,
    EntangledModelForm,
):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "figure_caption",
                "figure_alignment",
                "attributes",
            ]
        }

    figure_caption = HTMLFormField(
        label=_("Caption"),
        initial="",
        required=True,
    )
    figure_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
