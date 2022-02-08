from djangocms_frontend.frontends.foundation6 import convert_context


class AlertRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("callout", convert_context(instance.alert_context))
        return super().render(context, instance, placeholder)
