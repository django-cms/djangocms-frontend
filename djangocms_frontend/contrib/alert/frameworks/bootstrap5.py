from copy import deepcopy

from django.forms import fields
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings


class AlertRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "alert alert-{}".format(instance.alert_context)
        if instance.alert_dismissible:
            context["add_classes"] += " alert-dismissible"
        return super().render(context, instance, placeholder)
