from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.helpers import insert_fields

AUTO_SIZE = (("auto", _("Auto")),)


class SizingMixin:
    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            (("size_x", "size_y"),),
            block=0,  # Add to first fieldset - no own tab
            position=-1,
        )

    def render(self, context, instance, placeholder):
        size_x = instance.config.get("size_x", "")
        if size_x.isnumeric() or size_x == "auto":
            instance.add_classes(f"w-{size_x}")
        else:
            instance.add_classes(size_x)
        size_y = instance.config.get("size_y", "")
        if size_y.isnumeric() or size_y == "auto":
            instance.add_classes(f"h-{size_y}")
        else:
            instance.add_classes(size_y)
        return super().render(context, instance, placeholder)


class SizingFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "size_x",
                "size_y",
            ]
        }

    size_x = forms.ChoiceField(
        label=_("Horizontal size"),
        required=False,
        initial=settings.EMPTY_CHOICE[0][0],
        choices=settings.EMPTY_CHOICE + settings.SIZE_X_CHOICES,
        #        widget=ButtonGroup(attrs=dict(property="text")),
        help_text=_("Sets the horizontal size relative to the surrounding container or the viewport."),
    )
    size_y = forms.ChoiceField(
        label=_("Vertical size"),
        required=False,
        initial=settings.EMPTY_CHOICE[0][0],
        choices=settings.EMPTY_CHOICE + settings.SIZE_Y_CHOICES,
        #       widget=ButtonGroup(attrs=dict(property="text")),
        help_text=_("Sets the vertical size relative to the surrounding container or the viewport."),
    )
