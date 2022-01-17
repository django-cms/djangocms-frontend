from copy import deepcopy

from django.forms import fields
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.helpers import insert_fields


class AlertRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "alert alert-{}".format(instance.alert_context)
        if instance.alert_dismissible:
            context["add_classes"] += " alert-dismissible"
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        fs = deepcopy(self.fieldsets)
        fs[0][1]["fields"][-1] = ("alert_dismissible", "alert_icon")
        return fs


class AlertFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "alert_icon",
            ]
        }

    alert_icon = fields.ChoiceField(
        label=_("Icon"),
        required=False,
        choices=settings.EMPTY_CHOICE
        + (
            ("check", _("Check")),
            ("info", _("Information")),
            ("exclamation", _("Exclamation")),
        ),
        help_text=_("Adds an icon at teh left of the alert."),
    )
