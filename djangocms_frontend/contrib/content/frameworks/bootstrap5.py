class BlockquoteRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = (
            f"text-{instance.quote_alignment}" if instance.quote_alignment else ""
        )
        return super().render(context, instance, placeholder)


class FigureRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "figure"
        context["figure_alignment"] = (
            f"text-{instance.figure_alignment}" if instance.figure_alignment else ""
        )
        return super().render(context, instance, placeholder)
