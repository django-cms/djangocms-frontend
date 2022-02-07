class MediaRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/media.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("d-flex")
        return super().render(context, instance, placeholder)


class MediaBodyRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("flex-grow-1", "ms-3")
        return super().render(context, instance, placeholder)
