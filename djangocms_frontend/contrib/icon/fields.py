import json

from cms.utils.urlutils import static_with_version
from django.forms.fields import JSONField, TextInput

from djangocms_frontend.contrib.icon.conf import ICON_LIBRARIES


class IconPickerWidget(TextInput):  # pragma: no cover
    class Media:
        js = ("djangocms_frontend/icon/vendor/assets/js/universal-icon-picker.min.js",)
        css = {"all": (static_with_version("cms/css/cms.icons.css"),)}

    template_name = "djangocms_frontend/admin/widgets/icon_picker.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            json_obj = json.loads(value) or {}
        except ValueError:
            json_obj = {}
        context["widget"]["preview"] = json_obj.get("iconHtml", "")
        context["widget"]["library"] = json_obj.get("library", "")
        context["icon_libraries"] = [
            (key, key.title(), value[0], value[1])
            for key, value in ICON_LIBRARIES.items()
        ]
        return context


class IconPickerField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", IconPickerWidget)
        super().__init__(*args, **kwargs)
