class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "grid-container"
        if instance.container_type != "container":
            context["add_classes"] += "fluid"
        return super().render(context, instance, placeholder)
