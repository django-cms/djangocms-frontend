try:
    from functools import cached_property
except ImportError:  # Only available since Python 3.8
    cached_property = property

from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from djangocms_frontend.models import FrontendUIItem

from .constants import GRID_CONTAINER_CHOICES


class TitleModelMixin:
    pass


class GridContainer(TitleModelMixin, FrontendUIItem):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Container")
        _("GridContainer")

    def get_short_description(self):
        text = self.config.get("plugin_title", {}).get("title", "") or self.config.get("attributes", {}).get("id", "")
        for item in GRID_CONTAINER_CHOICES[1:]:
            if item[0] == self.container_type:
                text += f" ({item[1]})"
        return text


class GridRow(TitleModelMixin, FrontendUIItem):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Row")
        _("GridRow")

    def get_short_description(self):
        descr = self.config.get("plugin_title", {}).get("title", "") or self.config.get("attributes", {}).get("id", "")
        column_count = len(self.child_plugin_instances or [])
        column_count_str = ngettext("(1 column)", "(%(count)i columns)", column_count) % {"count": column_count}
        if descr:
            column_count_str = f"{descr} {column_count_str}"
        return column_count_str


class GridColumn(FrontendUIItem):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    class Meta:
        proxy = True
        verbose_name = _("Column")
        _("GridColumn")

    def get_short_description(self):
        text = self.config.get("plugin_title", {}).get("title", "") or self.config.get("attributes", {}).get("id", "")

        if self.config.get("xs_col"):
            text += f" (col-{self.xs_col}) "
        else:
            text += " (auto) "
        return text.strip()
