from copy import copy

from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.helpers import mark_safe_lazy

from ... import settings
from ...fields import AttributesFormField
from ...models import FrontendUIItem
from .. import grid
from .constants import (
    GRID_COLUMN_ALIGNMENT_CHOICES,
    GRID_COLUMN_CHOICES,
    GRID_CONTAINER_CHOICES,
    GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
    GRID_ROW_VERTICAL_ALIGNMENT_CHOICES,
    GRID_SIZE,
)

mixin_factory = settings.get_forms(grid)


class GridContainerForm(mixin_factory("GridContainer"), EntangledModelForm):
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


class GridRowBaseForm(mixin_factory("GridRow"), EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "create",
                "vertical_alignment",
                "horizontal_alignment",
                "gutters",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

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
        help_text=mark_safe_lazy(
            _(
                'Read more in the <a href="{link}" target="_blank">documentation</a>.'
            ).format(
                link="https://getbootstrap.com/docs/5.0/layout/grid/#vertical-alignment"
            )
        ),
    )
    horizontal_alignment = forms.ChoiceField(
        label=_("Horizontal alignment"),
        choices=settings.EMPTY_CHOICE + GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
        required=False,
        help_text=mark_safe_lazy(
            _(
                'Read more in the <a href="{link}" target="_blank">documentation</a>.'
            ).format(
                link="https://getbootstrap.com/docs/5.0/layout/grid/#horizontal-alignment"
            )
        ),
    )
    gutters = forms.BooleanField(
        label=_("Remove gutters"),
        initial=False,
        required=False,
        help_text=_("Removes the marginal gutters from the grid."),
    )
    attributes = AttributesFormField()


# convert regular text type fields to number
extra_fields_column = {}
for size in settings.DEVICE_SIZES:
    extra_fields_column["row_cols_{}".format(size)] = forms.IntegerField(
        label="row-cols" if size == "xs" else "row-cols-{}".format(size),
        required=False,
        min_value=1,
        max_value=GRID_SIZE,
    )

GridRowForm = type(
    str("GridRowBaseForm"),
    (GridRowBaseForm,),
    copy(extra_fields_column),
)

GridRowForm.Meta.entangled_fields["config"] += extra_fields_column.keys()


class GridColumnBaseForm(mixin_factory("GridColumn"), EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "column_type",
                "column_alignment",
                "text_alignment",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    column_type = forms.ChoiceField(
        label=_("Column type"),
        choices=GRID_COLUMN_CHOICES,
        initial=GRID_COLUMN_CHOICES[0][0],
        required=True,
    )
    column_alignment = forms.ChoiceField(
        label=_("Column alignment"),
        choices=settings.EMPTY_CHOICE + GRID_COLUMN_ALIGNMENT_CHOICES,
        required=False,
    )
    text_alignment = forms.ChoiceField(
        label=_("Content alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()


# convert regular text type fields to number
extra_fields_column = {}
for size in settings.DEVICE_SIZES:
    extra_fields_column["{}_col".format(size)] = forms.IntegerField(
        label="col" if size == "xs" else "col-{}".format(size),
        required=False,
        min_value=1,
        max_value=GRID_SIZE,
    )
    extra_fields_column["{}_order".format(size)] = forms.IntegerField(
        label="order" if size == "xs" else "order-{}".format(size),
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
    )
    extra_fields_column["{}_offset".format(size)] = forms.IntegerField(
        label="offset" if size == "xs" else "offset-{}".format(size),
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
    )
    extra_fields_column["{}_ml".format(size)] = forms.BooleanField(
        label="ml-auto" if size == "xs" else "ml-{}-auto".format(size),
        required=False,
    )
    extra_fields_column["{}_mr".format(size)] = forms.BooleanField(
        label="mr-auto" if size == "xs" else "mr-{}-auto".format(size),
        required=False,
    )

GridColumnForm = type(
    str("GridColumnForm"),
    (GridColumnBaseForm,),
    copy(extra_fields_column),
)

GridColumnForm.Meta.entangled_fields["config"] += extra_fields_column.keys()
