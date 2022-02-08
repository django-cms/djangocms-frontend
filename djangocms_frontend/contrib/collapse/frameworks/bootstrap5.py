class CollapseRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/collapse.html"


class CollapseContainerRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/collapse-container.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("collapse")
        return super().render(context, instance, placeholder)


class CollapseTriggerRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/collapse-trigger.html"
