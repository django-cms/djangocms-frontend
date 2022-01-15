
class RenderAlertMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "alert alert-{}".format(instance.alert_context)
        if instance.alert_dismissible:
            context["add_classes"] += " alert-dismissible"
        return super().render(context, instance, placeholder)
