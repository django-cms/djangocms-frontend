class JumbotronRenderMixin:
    def render(self, context, instance, placeholder):
        if not getattr(instance, "background_context", False):
            instance.add_classes("bg-light")
        return super().render(context, instance, placeholder)
