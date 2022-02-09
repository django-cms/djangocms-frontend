from djangocms_frontend.frameworks.foundation6 import convert_context


class AlertRenderMixin:
    render_template = "djangocms_frontend/foundation6/alert.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("callout", convert_context(instance.alert_context))
        if instance.alert_dismissible:
            instance.add_attribute("data-closable")
        return super().render(context, instance, placeholder)
