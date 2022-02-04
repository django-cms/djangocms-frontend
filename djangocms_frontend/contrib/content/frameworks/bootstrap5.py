class BlockquoteRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("blockquote")
        if instance.quote_alignment:
            instance.add_classes(f"text-{instance.quote_alignment}")
        return super().render(context, instance, placeholder)


class FigureRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("figure")
        if instance.figure_alignment:
            instance.add_classes(f"text-{instance.figure_alignment}")
        return super().render(context, instance, placeholder)
