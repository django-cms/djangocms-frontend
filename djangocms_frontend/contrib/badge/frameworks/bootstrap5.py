class BadgeRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(f"badge bg-{instance.badge_context}")
        if instance.badge_pills:
            instance.add_classes("rounded-pill")
        return super().render(context, instance, placeholder)
