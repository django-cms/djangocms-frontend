from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.contrib.grid.frameworks.bootstrap5 import (
    get_row_cols_grid_values,
)
from djangocms_frontend.fields import ButtonGroup
from djangocms_frontend.helpers import insert_fields


class CardRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/card.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("card")
        if instance.card_context and instance.card_outline:
            instance.add_classes(f"border-{instance.card_context}")
        elif instance.card_context:
            instance.add_classes(f"bg-{instance.card_context}")
            if getattr(instance, "card_opacity", "100") != "100":
                instance.add_classes(f"bg-opacity-{instance.card_opacity}")
        if getattr(instance, "card_shadow", ""):
            if instance.card_shadow == "reg":
                instance.add_classes("shadow")
            else:
                instance.add_classes(f"shadow-{instance.card_shadow}")
        if instance.card_alignment:
            instance.add_classes(f"text-{instance.card_alignment}")
        if instance.card_text_color:
            instance.add_classes(f"text-{instance.card_text_color}")
        if getattr(instance, "card_full_height", False):
            instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            (("card_opacity", "card_shadow"),),
            block=0,
            position=2,
        )


class CardFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "card_opacity",
                "card_shadow",
            ]
        }

    card_opacity = forms.ChoiceField(
        label=_("Background opacity"),
        required=False,
        choices=settings.framework_settings.OPACITY_CHOICES,
        initial=settings.framework_settings.OPACITY_CHOICES[0][0],
        widget=ButtonGroup(attrs=dict(property="opacity")),
        help_text=_("Opacity of card background color (only if no outline selected)"),
    )

    card_shadow = forms.ChoiceField(
        label=_("Shadow"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.framework_settings.SHADOW_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ButtonGroup(attrs=dict(property="shadow")),
        help_text=_("Use shadows to optically lift cards from the background."),
    )


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.inner_type)
        if getattr(instance, "inner_context", None):
            instance.add_classes(f"bg-{instance.inner_context}")
            if getattr(instance, "inner_opacity", "100") != "100":
                instance.add_classes(f"bg-opacity-{instance.inner_opacity}")
        if getattr(instance, "text_alignment", None):
            instance.add_classes(f"text-{instance.text_alignment}")
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            ("inner_opacity",),
            block=0,
            position=2,
        )


class CardInnerFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "inner_opacity",
            ]
        }

    inner_opacity = forms.ChoiceField(
        label=_("Background opacity"),
        required=False,
        choices=settings.framework_settings.OPACITY_CHOICES,
        initial=settings.framework_settings.OPACITY_CHOICES[0][0],
        widget=ButtonGroup(attrs=dict(property="opacity")),
        help_text=_("Opacity of card inner background color"),
    )


class CardLayoutRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.card_type)
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)
