from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import ButtonGroup
from djangocms_frontend.helpers import insert_fields


class JumbotronRenderMixin:
    def render(self, context, instance, placeholder):

        instance.add_classes("p-4", "my-0")
        if getattr(instance, "jumbotron_context", ""):
            instance.add_classes(f"bg-{instance.jumbotron_context}")
            if getattr(instance, "jumbotron_opacity", "100") != "100":
                instance.add_classes(f"bg-opacity-{instance.jumbotron_opacity}")
        else:
            instance.add_classes("bg-light")
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            ("jumbotron_opacity",),
            block=0,
            position=-1,
        )


class JumbotronFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "jumbotron_opacity",
            ]
        }

    jumbotron_opacity = forms.ChoiceField(
        label=_("Background opacity"),
        required=False,
        choices=settings.framework_settings.OPACITY_CHOICES,
        initial=settings.framework_settings.OPACITY_CHOICES[0][0],
        widget=ButtonGroup(attrs=dict(property="opacity")),
        help_text=_("Opacity of card background color (only if no outline selected)"),
    )
