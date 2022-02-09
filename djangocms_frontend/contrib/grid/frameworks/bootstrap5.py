from django import forms
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import ButtonGroup, ColoredButtonGroup
from djangocms_frontend.helpers import insert_fields


def get_row_cols_grid_values(instance):
    classes = []
    for device in settings.DEVICE_SIZES:
        size = getattr(instance, f"row_cols_{device}", None)
        if isinstance(size, int):
            if device == "xs":
                classes.append(f"row-cols-{int(size)}")
            else:
                classes.append(f"row-cols-{device}-{int(size)}")
    return classes


class GridContainerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.container_type)
        if getattr(instance, "container_context", ""):
            instance.add_classes(f"bg-{instance.container_context}")
        if getattr(instance, "container_opacity", "100") != "100":
            instance.add_classes(f"bg-opacity-{instance.container_opacity}")
        if getattr(instance, "container_shadow", ""):
            if instance.container_shadow == "reg":
                instance.add_classes("shadow")
            else:
                instance.add_classes(f"shadow-{instance.container_shadow}")
        return super().render(context, instance, placeholder)

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            (
                "container_context",
                ("container_opacity", "container_shadow"),
            ),
            block=None,
            position=-2,
            blockname=_("Background"),
        )


class GridContainerFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "container_context",
                "container_opacity",
                "container_shadow",
            ]
        }

    container_context = forms.ChoiceField(
        label=_("Background context"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE,
        help_text=_("Covers image."),
        widget=ColoredButtonGroup(),
    )
    container_opacity = forms.ChoiceField(
        label=_("Background opacity"),
        required=False,
        choices=settings.framework_settings.OPACITY_CHOICES,
        initial=settings.framework_settings.OPACITY_CHOICES[0][0],
        widget=ButtonGroup(attrs=dict(property="opacity")),
        help_text=_("Opacity of card background color (only if no outline selected)"),
    )

    container_shadow = forms.ChoiceField(
        label=_("Shadow"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.framework_settings.SHADOW_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=ButtonGroup(attrs=dict(property="shadow")),
        help_text=_("Use shadows to optically lift cards from the background."),
    )


class GridRowRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/grid_row.html"

    def render(self, context, instance, placeholder):
        instance.add_classes(
            "row",
            instance.vertical_alignment,
            instance.horizontal_alignment,
        )
        if instance.gutters or (
            instance.parent and instance.parent.plugin_type == "CardPlugin"
        ):  # no gutters if inside card
            instance.add_classes("g-0")
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)


def get_grid_values(self):
    classes = []
    for device in settings.DEVICE_SIZES:
        for element in ("col", "order", "offset", "ms", "me"):
            size = getattr(self, f"{device}_{element}", None)
            if isinstance(size, int) and (
                element == "col" or element == "order" or element == "offset"
            ):
                if size == 0 and element == "col":
                    size = "auto"
                if device == "xs":
                    classes.append(f"{element}-{size}")
                else:
                    classes.append(f"{element}-{device}-{size}")
            elif size:
                if device == "xs":
                    classes.append("{}-{}".format(element, "auto"))
                else:
                    classes.append("{}-{}-{}".format(element, device, "auto"))

    return classes


class GridColumnRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(
            f"col text-{instance.text_alignment}"
            if instance.config.get("text_alignment", None)
            else "col"
        )
        instance.add_classes(instance.column_alignment)
        instance.add_classes(get_grid_values(instance))
        return super().render(context, instance, placeholder)
