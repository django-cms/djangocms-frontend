from djangocms_frontend import settings
from djangocms_frontend.frameworks.bootstrap5_tokens import field_value, grid_value
from djangocms_frontend.models import is_plugin_type


def get_row_cols_grid_values(instance):
    classes = []
    for device in settings.DEVICE_SIZES:
        size = grid_value(instance, f"row_cols_{device}")
        if isinstance(size, int):
            if device == "xs":
                classes.append(f"row-cols-{int(size)}")
            else:
                classes.append(f"row-cols-{device}-{int(size)}")
    return classes


class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(field_value(instance, "container_type"))
        return super().render(context, instance, placeholder)


class GridRowRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/grid_row.html"

    def render(self, context, instance, placeholder):
        instance.add_classes(
            "row",
            field_value(instance, "vertical_alignment"),
            field_value(instance, "horizontal_alignment"),
        )
        if instance.parent and is_plugin_type(instance.parent.plugin_type, "CardPlugin"):
            instance.add_classes("g-0")  # no gutters if inside card
        gutters = field_value(instance, "gutters")
        if gutters:
            instance.add_classes(f"g-{gutters}")
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)


def get_grid_values(self):
    classes = []
    for device in settings.DEVICE_SIZES:
        for element in ("col", "order", "offset", "ms", "me"):
            size = grid_value(self, f"{device}_{element}")
            if isinstance(size, int) and (element == "col" or element == "order" or element == "offset"):
                if size == 0 and element == "col":  # 0 represents auto
                    size = "auto"
                if device == "xs":
                    classes.append(f"{element}-{size}")
                else:
                    classes.append(f"{element}-{device}-{size}")
            elif size:
                if device == "xs":
                    classes.append("{}-{}".format(element, "auto"))
                else:
                    classes.append("{}-{}-{}".format(element, device, "auto"))

    return classes


class GridColumnRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(
            f"col text-{instance.text_alignment}" if instance.config.get("text_alignment", None) else "col"
        )
        instance.add_classes(field_value(instance, "column_alignment"))
        instance.add_classes(get_grid_values(instance))
        return super().render(context, instance, placeholder)
