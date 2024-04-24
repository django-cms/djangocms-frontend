from djangocms_frontend import settings

foundation_sizes = dict(xs="small", md="medium", xl="large")


class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("grid-container")
        if instance.container_type == "container-fluid":
            instance.add_classes("fluid")
        elif instance.container_type != "container":
            instance.add_classss("full")
        return super().render(context, instance, placeholder)


def get_row_cols_grid_values(instance):
    classes = []
    for device in settings.DEVICE_SIZES:
        size = getattr(instance, f"row_cols_{device}", None)
        if isinstance(size, int):
            classes.append(f"{foundation_sizes.get(device, device)}-up-{int(size)}")
    return classes


class GridRowRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("grid-x", get_row_cols_grid_values(instance))
        if not instance.gutters:
            instance.add_classes("grid-padding-x", "grid-padding-y")
        return super().render(context, instance, placeholder)


def get_grid_values(self):
    classes = []
    for device in settings.DEVICE_SIZES:
        for element in ("col", "order", "offset"):
            size = getattr(self, f"{device}_{element}", None)
            if isinstance(size, int):
                if element == "col":
                    if size == 0:
                        classes.append(f"{foundation_sizes.get(device, device)}-auto")
                    else:
                        classes.append(f"{foundation_sizes.get(device, device)}-{size}")
                else:
                    classes.append(f"{foundation_sizes.get(device, device)}-{element}-{size}")

    return classes


class GridColumnRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("cell", get_grid_values(instance))
        return super().render(context, instance, placeholder)
