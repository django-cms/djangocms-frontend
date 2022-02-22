from copy import copy

from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.background import BackgroundFormMixin
from djangocms_frontend.common.responsive import ResponsiveFormMixin
from djangocms_frontend.common.sizing import SizingFormMixin
from djangocms_frontend.common.spacing import SpacingFormMixin
from djangocms_frontend.fields import AttributesFormField, IconGroup, TagTypeFormField
from djangocms_frontend.helpers import link_to_framework_doc, mark_safe_lazy
from djangocms_frontend.models import FrontendUIItem

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
        initial=GRID_CONTAINER_CHOICES[0][0],
        help_text=mark_safe_lazy(
            _(
                "Defines if the grid should use fixed width (<code>.container</code>) "
                "or fluid width (<code>.container-fluid</code>)."
            )
        ),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class GridRowBaseForm(
    mixin_factory("GridRow"), ResponsiveFormMixin, SpacingFormMixin, EntangledModelForm
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
    gutters = forms.BooleanField(
        label=_("Remove gutters"),
        initial=False,
        required=False,
        help_text=_("Removes the marginal gutters from the grid."),
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

GridRowForm = type(
    "GridRowBaseForm",
    (GridRowBaseForm,),
    copy(extra_fields_column),
)

GridRowForm.Meta.entangled_fields["config"] += extra_fields_column.keys()


class GridColumnBaseForm(
    mixin_factory("GridColumn"),
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


# convert regular text type fields to number
extra_fields_column = {}
for size in settings.DEVICE_SIZES:
    extra_fields_column[f"{size}_col"] = forms.IntegerField(
        label="col" if size == "xs" else f"col-{size}",
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
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
        widget=forms.HiddenInput()
        if "{size}_ms" in getattr(settings, "EXCL_COL_PROP", ())
        else forms.CheckboxInput(),
    )
    extra_fields_column[f"{size}_me"] = forms.BooleanField(
        label="me-auto" if size == "xs" else f"me-{size}-auto",
        required=False,
        widget=forms.HiddenInput()
        if "{size}_me" in getattr(settings, "EXCL_COL_PROP", ())
        else forms.CheckboxInput(),
    )

GridColumnForm = type(
    "GridColumnForm",
    (GridColumnBaseForm,),
    copy(extra_fields_column),
)

GridColumnForm.Meta.entangled_fields["config"] += extra_fields_column.keys()
