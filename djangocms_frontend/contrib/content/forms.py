from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import ALIGN_CHOICES

from ... import settings
from ...common.background import BackgroundFormMixin
from ...common.responsive import ResponsiveFormMixin
from ...common.spacing import SpacingFormMixin
from ...fields import AttributesFormField, IconGroup, TagTypeFormField
from ...models import FrontendUIItem
from .constants import CODE_TYPE_CHOICES


class CodeForm(
    SpacingFormMixin, ResponsiveFormMixin, BackgroundFormMixin, EntangledModelForm
):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

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
        initial=CODE_TYPE_CHOICES[0][0],
        required=True,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class BlockquoteForm(
    SpacingFormMixin, ResponsiveFormMixin, BackgroundFormMixin, EntangledModelForm
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

    quote_content = forms.CharField(
        label=_("Quote"),
        initial="",
        required=True,
        widget=forms.Textarea(),
    )
    quote_origin = forms.CharField(
        label=_("Cite"),
        required=False,
        widget=forms.Textarea(),
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
    SpacingFormMixin, ResponsiveFormMixin, BackgroundFormMixin, EntangledModelForm
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

    figure_caption = forms.CharField(
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
