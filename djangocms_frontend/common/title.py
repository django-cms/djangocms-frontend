from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin


class TitleWidget(forms.MultiWidget):  # lgtm [py/missing-call-to-init]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widgets",
            (
                forms.CheckboxInput(),
                forms.TextInput(),
            ),
        )
        super().__init__(*args, **kwargs)

    def decompress(self, value):
        if isinstance(value, dict):
            return [value.get("show", False), value.get("title", "")]
        return [False, ""]


class TitleField(forms.MultiValueField):  # lgtm [py/missing-call-to-init]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "fields",
            (
                forms.BooleanField(required=False),
                forms.CharField(required=False),
            ),
        )
        kwargs.setdefault("require_all_fields", False)
        kwargs.setdefault("widget", TitleWidget())
        super().__init__(*args, **kwargs)

    def clean(self, value):
        if value[0] and not value[1]:
            raise ValidationError(_("Please add a title if you want to publish it."), code="incomplete")
        return super().clean(value)

    def compress(self, data_list):
        return dict(show=data_list[0], title=data_list[1])


class TitleMixin:
    def render(self, context, instance, placeholder):
        if instance.config.get("plugin_title", {}).get("show", False):
            instance.add_attribute("title", instance.plugin_title.get("title", ""))
        return super().render(context, instance, placeholder)


class TitleFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "plugin_title",
            ]
        }

    plugin_title = TitleField(
        label=_("Title"),
        required=False,
        initial={"show": False, "title": ""},
        help_text=_(
            "Optional title of the plugin for easier identification. "
            "Its <code>title</code> attribute "
            "will only be set if the checkbox is selected."
        ),
    )
