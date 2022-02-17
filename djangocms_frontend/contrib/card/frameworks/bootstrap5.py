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
        if instance.config.get("card_outline", None):
            instance.add_classes(f"border-{instance.card_outline}")
        if instance.card_alignment:
            instance.add_classes(f"text-{instance.card_alignment}")
        if instance.config.get("card_text_color", None):
            instance.add_classes(f"text-{instance.card_text_color}")
        if instance.config.get("card_full_height", None):
            instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)


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
