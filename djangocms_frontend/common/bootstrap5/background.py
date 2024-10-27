from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import ButtonGroup, ColoredButtonGroup
from djangocms_frontend.helpers import insert_fields


class BackgroundMixin:
    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            (
                "background_context",
                ("background_opacity", "background_shadow"),
            ),
            block=None,
            position=-1,
            blockname=_("Background"),
        )

    def render(self, context, instance, placeholder):
        if getattr(instance, "background_context", ""):
            instance.add_classes(f"bg-{instance.background_context}")
        if getattr(instance, "background_opacity", ""):
            instance.add_classes(f"bg-opacity-{instance.background_opacity}")
        if getattr(instance, "background_shadow", ""):
            if instance.background_shadow == "reg":
                instance.add_classes("shadow")
            else:
                instance.add_classes(f"shadow-{instance.background_shadow}")
        return super().render(context, instance, placeholder)


class BackgroundFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "background_context",
                "background_opacity",
                "background_shadow",
            ]
        }

    background_context = forms.ChoiceField(
        label=_("Background context"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES + (("transparent", _("Transparent")),),
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ColoredButtonGroup(),
    )
    background_opacity = forms.ChoiceField(
        label=_("Background opacity"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.framework_settings.OPACITY_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ButtonGroup(attrs=dict(property="opacity")),
        help_text=_("Opacity of card background color (only if no outline selected)"),
    )

    background_shadow = forms.ChoiceField(
        label=_("Shadow"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.framework_settings.SHADOW_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ButtonGroup(attrs=dict(property="shadow")),
        help_text=_("Use shadows to optically lift cards from the background."),
    )
