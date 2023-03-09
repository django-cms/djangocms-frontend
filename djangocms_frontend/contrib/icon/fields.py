import json

from cms.utils.urlutils import static_with_version
from django.forms.fields import JSONField, TextInput

from djangocms_frontend.contrib.icon.conf import ICON_LIBRARIES_JSON, ICON_LIBRARIES_CSS


class IconPickerWidget(TextInput):
    class Media:
        js = ("djangocms_frontend/icon/vendor/assets/js/universal-icon-picker.min.js", )
        css = {"all": (static_with_version("cms/css/cms.icons.css"),)}

    template_name = "djangocms_frontend/admin/widgets/icon_picker.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            json_obj = json.loads(value) or {}
            preview = json_obj.get("iconHtml", "")
        except ValueError:
            preview = ""
        context["widget"]["preview"] = preview
        context["widget"]["icon_libraries"] = json.dumps(ICON_LIBRARIES_JSON)
        context["widget"]["icon_libraries_css"] = json.dumps(ICON_LIBRARIES_CSS)
        return context


class IconPickerField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", IconPickerWidget)
        super().__init__(*args, **kwargs)




