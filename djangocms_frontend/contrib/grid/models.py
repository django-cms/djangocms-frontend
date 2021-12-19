from functools import partial

from django.db import models
from django.utils.translation import ungettext

from djangocms_frontend.fields import IntegerRangeField
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import DEVICE_SIZES

from .constants import (
    GRID_COLUMN_ALIGNMENT_CHOICES,
    GRID_COLUMN_CHOICES,
    GRID_CONTAINER_CHOICES,
    GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
    GRID_ROW_VERTICAL_ALIGNMENT_CHOICES,
    GRID_SIZE,
)


class GridContainer(FrontendUIItem):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        text = ""
        for item in GRID_CONTAINER_CHOICES:
            if item[0] == self.container_type:
                text = item[1]
        return "({})".format(text)


class GridRow(FrontendUIItem):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        column_count = len(self.child_plugin_instances or [])
        column_count_str = ungettext(
            "(1 column)", "(%(count)i columns)", column_count
        ) % {"count": column_count}

        return column_count_str


class GridColumn(FrontendUIItem):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        text = ""
        classes = self.get_grid_values()
        if self.xs_col:
            text += "(col-{}) ".format(self.xs_col)
        else:
            text += "(auto) "
        if self.column_type != "col":
            text += ".{} ".format(self.column_type)
        if classes:
            text += ".{}".format(" .".join(self.get_grid_values()))
        return text

    def get_grid_values(self):
        classes = []
        for device in DEVICE_SIZES:
            for element in ("col", "order", "offset", "ml", "mr"):
                size = getattr(self, "{}_{}".format(device, element))
                if isinstance(size, int) and (
                    element == "col" or element == "order" or element == "offset"
                ):
                    if device == "xs":
                        classes.append("{}-{}".format(element, int(size)))
                    else:
                        classes.append("{}-{}-{}".format(element, device, int(size)))
                elif size:
                    if device == "xs":
                        classes.append("{}-{}".format(element, "auto"))
                    else:
                        classes.append("{}-{}-{}".format(element, device, "auto"))

        return classes
