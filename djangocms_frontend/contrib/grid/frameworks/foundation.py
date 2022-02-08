from djangocms_frontend import settings


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
        size = getattr(instance, "row_cols_{}".format(device), None)
        if isinstance(size, int):
            if device == "xs":
                classes.append("row-cols-{}".format(int(size)))
            else:
                classes.append("row-cols-{}-{}".format(device, int(size)))
    return classes


class GridRowContainerMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("grid-x")
        if not instance.gutters:
            instance.add_classes("grad-padding-x", "grid-padding-y")
        return super().render(context, instance, placeholder)
