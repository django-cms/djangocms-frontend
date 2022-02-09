from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import ButtonGroup
from djangocms_frontend.helpers import insert_fields


class AlertRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/alert.html"

    def render(self, context, instance, placeholder):
        instance.add_classes(f"alert alert-{instance.alert_context}")
        if getattr(instance, "alert_shadow", ""):
            if instance.alert_shadow == "reg":
                instance.add_classes("shadow")
            else:
                instance.add_classes(f"shadow-{instance.alert_shadow}")
        if instance.alert_dismissible:
            instance.add_classes("alert-dismissible")
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            ("alert_shadow",),
            block=0,
            position=1,
        )


class AlertFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "alert_shadow",
            ]
        }

    alert_shadow = forms.ChoiceField(
        label=_("Shadow"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.framework_settings.SHADOW_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ButtonGroup(attrs=dict(property="shadow")),
        help_text=_("Use shadows to optically lift alerts from the background."),
    )
