class CollapseContainerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("collapse")
        return super().render(context, instance, placeholder)
