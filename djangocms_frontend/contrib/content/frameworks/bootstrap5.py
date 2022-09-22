class BlockquoteRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/blockquote.html"

    def render(self, context, instance, placeholder):
        if not instance.config.get("quote_source", None):
            instance.add_classes("blockquote")
        if instance.quote_alignment:
            instance.add_classes(f"text-{instance.quote_alignment}")
        return super().render(context, instance, placeholder)


class FigureRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/figure.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("figure")
        if instance.figure_alignment:
            instance.add_classes(f"text-{instance.figure_alignment}")
        return super().render(context, instance, placeholder)


class CodeRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/code.html"
