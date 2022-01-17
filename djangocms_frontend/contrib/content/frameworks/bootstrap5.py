class BlockquoteRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "blockquote"
        if instance.quote_alignment:
            context["add_classes"] += instance.quote_alignment
        return super().render(context, instance, placeholder)


class FigureRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "figure"
        return super().render(context, instance, placeholder)
