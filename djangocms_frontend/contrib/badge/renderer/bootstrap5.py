class BadgeRenderMixin:
    def render(self, context, instance, placeholder):
        add_classes = f"badge bg-{instance.badge_context}"
        if instance.badge_pills:
            add_classes += " rounded-pill"
        context["add_classes"] = add_classes
        return super().render(context, instance, placeholder)
