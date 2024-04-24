class SpacingRenderMixin:
    def render(self, context, instance, placeholder):
        if not instance.space_device or instance.space_device == "xs":
            instance.add_classes(f"{instance.space_property}{instance.space_sides}-{instance.space_size}")
        else:
            instance.add_classes(
                f"{instance.space_property}{instance.space_sides}-{instance.space_device}-{instance.space_size}"
            )
        return super().render(context, instance, placeholder)


class EditorNoteRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/editor_note.html"


class HeadingRenderMixin:
    def render(self, context, instance, placeholder):
        heading_context = instance.config.get("heading_context", None)
        if heading_context:
            instance.add_classes(f"text-{heading_context}")
        heading_alignment = instance.config.get("heading_alignment", None)
        if heading_alignment:
            instance.add_classes(f"text-{heading_alignment}")
        return super().render(context, instance, placeholder)
