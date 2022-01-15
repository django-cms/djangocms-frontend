class CollapseContainerRenderMixin:
    def render(self, context, instance, placeholder):
         context["add_classes"] = "collapse"
         return super().render(context, instance, placeholder)
