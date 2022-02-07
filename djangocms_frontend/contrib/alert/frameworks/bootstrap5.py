class AlertRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/alert.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("alert alert-{}".format(instance.alert_context))
        if instance.alert_dismissible:
            instance.add_classes("alert-dismissible")
        return super().render(context, instance, placeholder)
