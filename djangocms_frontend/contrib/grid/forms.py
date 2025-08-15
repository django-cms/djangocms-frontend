from copy import copy

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common import BackgroundFormMixin, ResponsiveFormMixin, SizingFormMixin, SpacingFormMixin
from djangocms_frontend.fields import AttributesFormField, AutoNumberInput, ButtonGroup, IconGroup, TagTypeFormField
from djangocms_frontend.helpers import first_choice, link_to_framework_doc
from djangocms_frontend.models import FrontendUIItem

from ...common.title import TitleFormMixin
from .. import grid
from .constants import (
    GRID_COLUMN_ALIGNMENT_CHOICES,
    GRID_CONTAINER_CHOICES,
    GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
    GRID_ROW_VERTICAL_ALIGNMENT_CHOICES,
    GRID_SIZE,
)

mixin_factory = settings.get_forms(grid)


class GridContainerForm(
    mixin_factory("GridContainer"),
    TitleFormMixin,
    BackgroundFormMixin,
    ResponsiveFormMixin,
    SpacingFormMixin,
    SizingFormMixin,
    EntangledModelForm,
):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "container_type",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    container_type = forms.ChoiceField(
        label=_("Container type"),
        choices=GRID_CONTAINER_CHOICES,
        initial=first_choice(GRID_CONTAINER_CHOICES),
        help_text=_(
            "Defines if the grid should use fixed width, "
            "fluid width or the container should fill the full width without "
            "margins or padding."
        ),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class GridRowBaseForm(
    mixin_factory("GridRow"),
    TitleFormMixin,
    ResponsiveFormMixin,
    SpacingFormMixin,
    EntangledModelForm,
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "vertical_alignment",
                "horizontal_alignment",
                "gutters",
                "attributes",
            ]
        }
        untangled_fields = (
            "tag_type",
            "create",
        )

    create = forms.IntegerField(
        label=_("Create columns"),
        help_text=_("Number of columns to create when saving."),
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
    )
    vertical_alignment = forms.ChoiceField(
        label=_("Vertical alignment"),
        choices=settings.EMPTY_CHOICE + GRID_ROW_VERTICAL_ALIGNMENT_CHOICES,
        required=False,
        help_text=link_to_framework_doc("GridRow", "vertical_alignment_link"),
        widget=IconGroup(),
    )
    horizontal_alignment = forms.ChoiceField(
        label=_("Horizontal alignment"),
        choices=settings.EMPTY_CHOICE + GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
        required=False,
        help_text=link_to_framework_doc("GridRow", "horizontal_alignment_link"),
        widget=IconGroup(),
    )
    gutters = forms.ChoiceField(
        label=_("Gutters"),
        initial=settings.EMPTY_CHOICE[0][0],
        choices=settings.EMPTY_CHOICE + settings.SPACER_SIZE_CHOICES,
        required=False,
        help_text=_("To remove all spaces between rows set gutters to 0."),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


extra_fields_column = {}
for size in settings.DEVICE_SIZES:
    extra_fields_column[f"row_cols_{size}"] = forms.IntegerField(
        label="row-cols" if size == "xs" else f"row-cols-{size}",
        required=False,
        min_value=1,
        max_value=GRID_SIZE,
    )


GridRowBaseForm._meta.entangled_fields["config"] += extra_fields_column.keys()


GridRowForm = type(
    "GridRowForm",
    (GridRowBaseForm,),
    copy(extra_fields_column),
)

GridRowForm._meta.model = FrontendUIItem  # Potentially a django-entangled bug?


class GridColumnBaseForm(
    mixin_factory("GridColumn"),
    TitleFormMixin,
    BackgroundFormMixin,
    ResponsiveFormMixin,
    SpacingFormMixin,
    EntangledModelForm,
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "column_alignment",
                "text_alignment",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    column_alignment = forms.ChoiceField(
        label=_("Column alignment"),
        choices=settings.EMPTY_CHOICE + GRID_COLUMN_ALIGNMENT_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    text_alignment = forms.ChoiceField(
        label=_("Content alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

    def clean(self):
        super().clean()
        for size in settings.DEVICE_SIZES:
            if f"{size}_col" in self.cleaned_data:
                if isinstance(self.cleaned_data[f"{size}_col"], str) and self.cleaned_data[f"{size}_col"].isnumeric():
                    self.cleaned_data[f"{size}_col"] = int(self.cleaned_data[f"{size}_col"])
            else:
                raise ValidationError(
                    _('Column size needs to be empty, "auto", or a number between 1 and %(cols)d'),
                    params=dict(cols=GRID_SIZE),
                    code="invalid_column",
                )


# convert regular text type fields to number
# col_choices = [(col + 1, str(col + 1)) for col in range(GRID_SIZE)] + [("auto", "Auto")]
extra_fields_column = {}
for size in settings.DEVICE_SIZES:
    extra_fields_column[f"{size}_col"] = forms.IntegerField(
        label="col" if size == "xs" else f"col-{size}",
        required=False,
        initial="",
        min_value=0,
        max_value=GRID_SIZE,
        widget=AutoNumberInput(),
    )
    extra_fields_column[f"{size}_order"] = forms.IntegerField(
        label="order" if size == "xs" else f"order-{size}",
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
        widget=forms.HiddenInput()
        if "{size}_order" in getattr(settings, "EXCL_COL_PROP", ())
        else forms.NumberInput(),
    )
    extra_fields_column[f"{size}_offset"] = forms.IntegerField(
        label="offset" if size == "xs" else f"offset-{size}",
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
        widget=forms.HiddenInput()
        if "{size}_offset" in getattr(settings, "EXCL_COL_PROP", ())
        else forms.NumberInput(),
    )
    extra_fields_column[f"{size}_ms"] = forms.BooleanField(
        label="ms-auto" if size == "xs" else f"ms-{size}-auto",
        required=False,
        widget=forms.HiddenInput() if "{size}_ms" in getattr(settings, "EXCL_COL_PROP", ()) else forms.CheckboxInput(),
    )
    extra_fields_column[f"{size}_me"] = forms.BooleanField(
        label="me-auto" if size == "xs" else f"me-{size}-auto",
        required=False,
        widget=forms.HiddenInput() if "{size}_me" in getattr(settings, "EXCL_COL_PROP", ()) else forms.CheckboxInput(),
    )

GridColumnBaseForm._meta.entangled_fields["config"] += extra_fields_column.keys()

GridColumnForm = type(
    "GridColumnForm",
    (GridColumnBaseForm,),
    copy(extra_fields_column),
)

GridColumnForm._meta.model = FrontendUIItem  # Potentially a django-entangled bug?
