from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.common import AttributesMixin, BackgroundMixin, ResponsiveMixin, SizingMixin, SpacingMixin

from ...cms_plugins import CMSUIPlugin
from ...common import TitleMixin
from ...helpers import add_plugin
from .. import grid
from . import forms, models

mixin_factory = settings.get_renderer(grid)


@plugin_pool.register_plugin
class GridContainerPlugin(
    mixin_factory("GridContainer"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    SizingMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Container")
    module = _("Frontend")
    model = models.GridContainer
    form = forms.GridContainerForm
    change_form_template = "djangocms_frontend/admin/grid_container.html"
    allow_children = True
    show_add_form = False

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "container_type",
                        "plugin_title",
                    ),
                )
            },
        ),
    ]


@plugin_pool.register_plugin
class GridRowPlugin(
    mixin_factory("GridRow"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Row")
    module = _("Frontend")
    model = models.GridRow
    form = forms.GridRowForm
    change_form_template = "djangocms_frontend/admin/grid_row.html"
    allow_children = True
    child_classes = ["GridColumnPlugin", "CardPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "create",
                        "plugin_title",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": ([f"row_cols_{size}" for size in settings.DEVICE_SIZES],),
            },
        ),
        (
            _("Alignment"),
            {
                "fields": (
                    ("vertical_alignment", "horizontal_alignment"),
                    "gutters",
                ),
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for pos in range(data["create"] if data["create"] is not None else 0):
            extra = dict(column_alignment=None)
            for size in settings.DEVICE_SIZES:
                extra[f"{size}_col"] = data.get(f"create_{size}_col")
                extra[f"{size}_order"] = None
                extra[f"{size}_offset"] = None
                extra[f"{size}_ml"] = None
                extra[f"{size}_mr"] = None
            add_plugin(
                obj.placeholder,
                models.GridColumn(
                    parent=obj,
                    placeholder=obj.placeholder,
                    position=obj.position + pos + 1,
                    language=obj.language,
                    plugin_type=GridColumnPlugin.__name__,
                    ui_item=models.GridColumn.__class__.__name__,
                    config=extra,
                ),
            )


@plugin_pool.register_plugin
class GridColumnPlugin(
    mixin_factory("GridColumn"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    TitleMixin,
    CMSUIPlugin,
):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Column")
    module = _("Frontend")
    model = models.GridColumn
    form = forms.GridColumnForm
    change_form_template = "djangocms_frontend/admin/grid_column.html"
    allow_children = True
    require_parent = True
    # TODO it should allow for the responsive utility class
    # https://getbootstrap.com/docs/5.0/layout/grid/#column-resets
    parent_classes = ["GridRowPlugin"]
    show_add_form = False

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "column_alignment",
                        "text_alignment",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": (
                    [f"{size}_col" for size in settings.DEVICE_SIZES],
                    [f"{size}_order" for size in settings.DEVICE_SIZES],
                    [f"{size}_offset" for size in settings.DEVICE_SIZES],
                    [f"{size}_ms" for size in settings.DEVICE_SIZES],
                    [f"{size}_me" for size in settings.DEVICE_SIZES],
                )
            },
        ),
        (_("Title settings"), {"fields": ("plugin_title",)}),
    ]
