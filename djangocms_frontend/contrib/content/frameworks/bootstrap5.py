class BlockquoteRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = (
            instance.quote_alignment if instance.quote_alignment else ""
        )
        return super().render(context, instance, placeholder)


class FigureRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "figure"
        return super().render(context, instance, placeholder)
