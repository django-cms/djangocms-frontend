from functools import partial

from djangocms_frontend.frameworks.bootstrap5_tokens import field_value


class SpacingRenderMixin:
    def render(self, context, instance, placeholder):
        # Shares the class rule with the structure board description, including overrides.
        get_base_css_class = getattr(instance, "get_base_css_class", None)
        if get_base_css_class is None:
            from djangocms_frontend.contrib.utilities.models import Spacing

            get_base_css_class = partial(Spacing.get_base_css_class, instance)
        instance.add_classes(get_base_css_class())
        return super().render(context, instance, placeholder)


class EditorNoteRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/editor_note.html"


class HeadingRenderMixin:
    def render(self, context, instance, placeholder):
        heading_context = field_value(instance, "heading_context")
        if heading_context:
            instance.add_classes(f"text-{heading_context}")
        heading_alignment = instance.config.get("heading_alignment", None)
        if heading_alignment:
            instance.add_classes(f"text-{heading_alignment}")
        return super().render(context, instance, placeholder)
