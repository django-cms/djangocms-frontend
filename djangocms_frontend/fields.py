from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_attributes_field import fields

from . import settings


class ButtonGroup(forms.RadioSelect):
    template_name = "djangocms_frontend/admin/widgets/button_group.html"
    option_template_name = "djangocms_frontend/admin/widgets/button_group_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}


class ColoredButtonGroup(ButtonGroup):
    option_template_name = (
        "djangocms_frontend/admin/widgets/button_group_color_option.html"
    )

    class Media:
        css = settings.ADMIN_CSS

    def __init__(self, *args, **kwargs):
        kwargs.update({"attrs": {**kwargs.get("attrs", {}), **dict(property="color")}})
        super().__init__(*args, **kwargs)


class IconGroup(ButtonGroup):
    option_template_name = "djangocms_frontend/admin/widgets/icon_group_option.html"

    def __init__(self, *args, **kwargs):
        kwargs.update({"attrs": {**dict(property="icon"), **kwargs.get("attrs", {})}})
        super().__init__(*args, **kwargs)


class IconMultiselect(forms.CheckboxSelectMultiple):
    template_name = "djangocms_frontend/admin/widgets/button_group.html"
    option_template_name = "djangocms_frontend/admin/widgets/icon_group_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}

    def __init__(self, *args, **kwargs):
        kwargs.update({"attrs": {**kwargs.get("attrs", {}), **dict(property="icon")}})
        super().__init__(*args, **kwargs)


class OptionalDeviceChoiceField(forms.MultipleChoiceField):
    def __init__(self, **kwargs):
        kwargs.setdefault("choices", settings.DEVICE_CHOICES)
        kwargs.setdefault("initial", None)
        kwargs.setdefault("widget", IconMultiselect())
        super().__init__(**kwargs)

    def prepare_value(self, value):
        if value is None:
            value = [size for size, _ in settings.DEVICE_CHOICES]
        return super().prepare_value(value)

    def clean(self, value):
        value = super().clean(value)
        if len(value) == len(settings.DEVICE_CHOICES):
            return None
        return value


class DeviceChoiceField(OptionalDeviceChoiceField):
    def clean(self, value):
        value = super().clean(value)
        if isinstance(value, list) and len(value) == 0:
            raise ValidationError(
                _("Please select at least one device size"), code="invalid"
            )
        return value


class AttributesField(fields.AttributesField):
    def __init__(self, *args, **kwargs):
        if "verbose_name" not in kwargs:
            kwargs["verbose_name"] = _("Attributes")
        if "blank" not in kwargs:
            kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class AttributesFormField(fields.AttributesFormField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _("Attributes"))
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", fields.AttributesWidget)
        self.excluded_keys = kwargs.pop("excluded_keys", [])
        super().__init__(*args, **kwargs)


class TagTypeField(models.CharField):
    def __init__(self, *args, **kwargs):
        if "verbose_name" not in kwargs:
            kwargs["verbose_name"] = _("Tag type")
        if "choices" not in kwargs:
            kwargs["choices"] = settings.TAG_CHOICES
        if "default" not in kwargs:
            kwargs["default"] = settings.TAG_CHOICES[0][0]
        if "max_length" not in kwargs:
            kwargs["max_length"] = 255
        if "help_text" not in kwargs:
            kwargs["help_text"] = _("Select the HTML tag to be used.")
        super().__init__(*args, **kwargs)


class TagTypeFormField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _("Tag type"))
        kwargs.setdefault("choices", settings.TAG_CHOICES)
        kwargs.setdefault("initial", settings.TAG_CHOICES[0][0])
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", ButtonGroup(attrs=dict(property="text")))
        super().__init__(*args, **kwargs)
