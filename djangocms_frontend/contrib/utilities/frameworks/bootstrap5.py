class SpacingRenderMixin:
    def render(self, context, instance, placeholder):
        if not instance.space_device or instance.space_device == "xs":
            instance.add_classes(
                f"{instance.space_property}{instance.space_sides}-{instance.space_size}"
            )
        else:
            instance.add_classes(
                f"{instance.space_property}{instance.space_sides}-{ instance.space_device }-{instance.space_size}"
            )
        return super().render(context, instance, placeholder)
