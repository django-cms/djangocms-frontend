from djangocms_frontend.frameworks.bootstrap5_tokens import field_value


class BadgeRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("badge")
        color = field_value(instance, "badge_context")
        if color:
            instance.add_classes(f"bg-{color}")
        if instance.badge_pills:
            instance.add_classes("rounded-pill")
        return super().render(context, instance, placeholder)
