from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.settings import ALIGN_CHOICES

from ... import settings
from ...models import FrontendUIItem
from .constants import CODE_TYPE_CHOICES


class CodeForm(EntangledModelForm):
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
            ]
        }
        untangled_fields = (
            "tag_type",
            "attributes",
        )

    code_content = forms.CharField(
        label=_("Code"),
        widget=forms.widgets.Textarea(attrs={"class": "js-ckeditor-use-selected-text"}),
    )
    code_type = forms.ChoiceField(
        label=_("Code type"),
        choices=CODE_TYPE_CHOICES,
        initial=CODE_TYPE_CHOICES[0][0],
    )


class BlockquoteForm(EntangledModelForm):
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
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    quote_content = forms.CharField(
        label=_("Quote"),
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
    )


class FigureForm(EntangledModelForm):
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
            ]
        }
        untangled_fields = ("tag_type", "attributes")

    figure_caption = forms.CharField(
        label=_("Caption"),
    )
    figure_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=ALIGN_CHOICES,
        initial=ALIGN_CHOICES[0][0],
        required=False,
    )
