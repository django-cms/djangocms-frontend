from djangocms_frontend import settings


class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = f"bg-{instance.container_context}" if getattr(instance, "container_context", False) else ""
        return super().render(context, instance, placeholder)


class GridRowRenderMixin:
    def render(self, context, instance, placeholder):
        def get_grid_values(instance):
            classes = []
            for device in settings.DEVICE_SIZES:
                size = getattr(instance, "row_cols_{}".format(device), None)
                if isinstance(size, int):
                    if device == "xs":
                        classes.append("row-cols-{}".format(int(size)))
                    else:
                        classes.append("row-cols-{}-{}".format(device, int(size)))
            return classes

        add_classes = [
            "row",
            instance.vertical_alignment,
            instance.horizontal_alignment,
            "g-0"
            if instance.gutters  # no gutters if inside card
            or (instance.parent and instance.parent.plugin_type == "CardPlugin")
            else "",
        ]
        context["add_classes"] = " ".join(cls for cls in add_classes if cls)
        context["grid_classes"] = " ".join(get_grid_values(instance))
        return super().render(context, instance, placeholder)
