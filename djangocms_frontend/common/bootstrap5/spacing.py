from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import DeviceChoiceField, IconGroup
from djangocms_frontend.helpers import insert_fields
from djangocms_frontend.settings import DEVICE_CHOICES

AUTO_SIZE = (("auto", _("Auto")),)


class DivSelectWidget(forms.Select):
    """Select widget contained in a div for simple styling purposes"""

    template_name = "djangocms_frontend/admin/widgets/select.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/div_select.css",)}


class SizeSideWidget(forms.MultiWidget):  # lgtm [py/missing-call-to-init]
    """2 component widget allowing to choose a side and the size of a spacing"""

    def __init__(self, **kwargs):
        self.property = kwargs.pop("property")
        self.side_choices = kwargs.pop("side_choices")
        super().__init__(
            [
                IconGroup(choices=[(self.property + side, verbose) for side, verbose in self.side_choices]),
                DivSelectWidget(choices=kwargs.pop("size_choices")),
            ],
            **kwargs,
        )

    def decompress(self, value):
        if isinstance(value, str) and value:
            return value.split("-", 1)
        return ["", ""]  # [self.property+self.side_choices[0][0], ""]


class SpacingSizeSideField(forms.MultiValueField):  # lgtm [py/missing-call-to-init]
    """Field for spacing information using SizeSideWidget"""

    def __init__(self, **kwargs):
        size_choices = settings.EMPTY_CHOICE + kwargs.pop("size_choices")
        side_choices = kwargs.pop("side_choices")
        prop = kwargs.pop("property")
        kwargs.setdefault(
            "fields",
            (
                forms.ChoiceField(
                    choices=[(prop + side, verbose) for side, verbose in side_choices],
                ),
                forms.ChoiceField(choices=size_choices, required=False),
            ),
        )
        kwargs.setdefault(
            "widget",
            SizeSideWidget(
                property=prop,
                size_choices=size_choices,
                side_choices=side_choices,
            ),
        )
        kwargs.setdefault("require_all_fields", False)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)

    def compress(self, data_list):
        if data_list and data_list[1]:  # Size selected?
            return f"{data_list[0]}-{data_list[1]}"
        return ""

    def clean(self, value):
        value = value or ["", ""]
        if value[1] and not value[0]:
            raise ValidationError(
                _("Please choose a side to which the spacing should be applied."),
                code="incomplete",
            )
        return super().clean(value)


def get_spacing_classes(spacing_set, active_set=None):
    """Generates the necessary bootstrap spacing utility classes"""

    if active_set is None or len(active_set) == len(DEVICE_CHOICES):
        return [spacing for spacing in spacing_set if spacing[-1] != "-"]

    classes = []
    active = False
    for spacing in spacing_set:
        for device, __ in DEVICE_CHOICES:
            if (device in active_set) != active:
                active = device in active_set
                if device == "xs":
                    if spacing[-1] != "-":
                        classes.append(spacing)
                else:
                    left, right = spacing.rsplit("-", 1)
                    if right:
                        classes.append(f"{left}-{device}-{right if active else '0'}")
    return classes


class MarginMixin:
    blockname = _("Margin")

    def get_fieldsets(self, request, obj=None):
        return insert_fields(
            super().get_fieldsets(request, obj),
            (("margin_x", "margin_y"), "margin_devices"),
            block=None,
            position=-1,
            blockname=self.blockname,
        )

    def render(self, context, instance, placeholder):
        instance.add_classes(
            get_spacing_classes(
                [
                    instance.config[field]
                    for field in ("margin_x", "margin_y")
                    if field in instance.config and instance.config[field]
                ],
                instance.config.get("margin_devices", None),
            )
        )
        return super().render(context, instance, placeholder)


class PaddingMixin:
    blockname = _("Padding")

    def get_fieldsets(self, request, obj=None):
        blockname = self.blockname
        blockattrs = dict()
        fs = super().get_fieldsets(request, obj)
        for label, fields in fs:  # noqa
            if label == blockname:  # already included MarginMixin
                blockname = _("Padding")
                blockattrs = dict(classes=())
                break

        return insert_fields(
            fs,
            (("padding_x", "padding_y"), "padding_devices"),
            block=None,
            position=-1,
            blockname=blockname,
            blockattrs=blockattrs,
        )

    def render(self, context, instance, placeholder):
        instance.add_classes(
            get_spacing_classes(
                [
                    instance.config[field]
                    for field in ("padding_x", "padding_y")
                    if field in instance.config and instance.config[field]
                ],
                instance.config.get("padding_devices", None),
            )
        )
        return super().render(context, instance, placeholder)


class SpacingMixin(PaddingMixin, MarginMixin):
    blockname = _("Spacing")


class MarginFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "margin_x",
                "margin_y",
                "margin_devices",
            ]
        }

    margin_x = SpacingSizeSideField(
        label=_("Horizontal margin"),
        property="m",
        size_choices=settings.SPACER_SIZE_CHOICES + AUTO_SIZE,
        side_choices=settings.SPACER_X_SIDES_CHOICES,
    )
    margin_y = SpacingSizeSideField(
        label=_("Vertical margin"),
        property="m",
        size_choices=settings.SPACER_SIZE_CHOICES + AUTO_SIZE,
        side_choices=settings.SPACER_Y_SIDES_CHOICES,
    )
    margin_devices = DeviceChoiceField(
        label=_("Apply margin on device"),
        required=False,
        initial=[size for size, _ in settings.DEVICE_CHOICES],
        help_text=_(
            "Select only devices on which the margin should be applied. On other devices "
            "larger than the first selected device the margin will be set to zero."
        ),
    )


class PaddingFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "padding_x",
                "padding_y",
                "padding_devices",
            ]
        }

    padding_x = SpacingSizeSideField(
        label=_("Horizontal padding"),
        property="p",
        size_choices=settings.SPACER_SIZE_CHOICES,
        side_choices=settings.SPACER_X_SIDES_CHOICES,
    )
    padding_y = SpacingSizeSideField(
        label=_("Vertical padding"),
        property="p",
        size_choices=settings.SPACER_SIZE_CHOICES,
        side_choices=settings.SPACER_Y_SIDES_CHOICES,
    )
    padding_devices = DeviceChoiceField(
        label=_("Apply padding on device"),
        required=False,
        initial=[size for size, _ in settings.DEVICE_CHOICES],
        help_text=_(
            "Select only devices on which the padding should be applied. On other devices "
            "larger than the first selected device the padding will be set to zero."
        ),
    )


class SpacingFormMixin(MarginFormMixin, PaddingFormMixin):
    pass
