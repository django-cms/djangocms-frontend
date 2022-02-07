class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("grid-container")
        if instance.container_type != "container":
            instance.add_classes("fluid")
        return super().render(context, instance, placeholder)
