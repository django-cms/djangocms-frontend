import json

from django.forms.fields import JSONField, TextInput
from django.templatetags.static import static

from djangocms_frontend.contrib.icon.conf import ICON_LIBRARIES, VENDOR_PATH


class IconPickerWidget(TextInput):  # pragma: no cover
    class Media:
        js = (f"{VENDOR_PATH}/js/universal-icon-picker.min.js",)

    template_name = "djangocms_frontend/admin/widgets/icon_picker.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            json_obj = json.loads(value) or {}
        except ValueError:
            json_obj = {}
        if isinstance(json_obj, str):
            # Probably djangocms_icon classes
            context["widget"]["preview"] = f'<i class="{json_obj}"></i>'
            context["widget"]["library"] = ""
        else:
            context["widget"]["preview"] = json_obj.get("iconHtml", "")
            context["widget"]["library"] = json_obj.get("library", "")
        context["icon_libraries"] = [
            (
                key,
                key.title(),
                static(f"{VENDOR_PATH}/icons-libraries/{value[0]}"),
                value[1] if "/" in value[1] else static(f"{VENDOR_PATH}/stylesheets/{value[1]}"),
            )
            for key, value in ICON_LIBRARIES.items()
        ]
        return context


class IconPickerField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", IconPickerWidget)
        super().__init__(*args, **kwargs)
