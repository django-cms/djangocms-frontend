from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_attributes_field import fields

from . import settings


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


class ColoredButtonGroup(forms.Select):
    """Includes ADMIN_CSS"""

    class Media:
        css = settings.ADMIN_CSS
