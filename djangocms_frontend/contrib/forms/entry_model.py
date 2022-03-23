import decimal

from cms.utils.compat import DJANGO_3_0
from django import forms
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

if DJANGO_3_0:
    from django_jsonfield_backport.models import JSONField
else:
    JSONField = models.JSONField


class CSValues(forms.CharField):
    class CSVWidget(forms.TextInput):
        def format_value(self, value):
            return ", ".join(value)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", CSValues.CSVWidget())
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = value.split(",")
        value = list(map(lambda x: x.strip(), value))
        return value


class FormEntry(models.Model):
    class Meta:
        verbose_name = _("Form entry")
        verbose_name_plural = _("Form entries")

    form_name = models.SlugField(
        verbose_name=_("Form"),
        blank=False,
    )
    form_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    entry_data = JSONField(
        default=dict,
        blank=True,
        encoder=DjangoJSONEncoder,
    )
    html_headers = JSONField(
        default=dict,
        blank=True,
    )
    entry_created_at = models.DateTimeField(auto_now_add=True)
    entry_updated_at = models.DateTimeField(auto_now=True)

    def get_admin_form(self):
        entangled_fields = []
        fields = {}
        for key, value in self.entry_data.items():
            if isinstance(value, str):
                entangled_fields.append(key)
                fields[key] = forms.CharField(
                    label=key,
                    widget=forms.TextInput if len(value) < 80 else forms.Textarea,
                    required=False,
                )
            elif isinstance(value, (list, tuple)):
                entangled_fields.append(key)
                fields[key] = CSValues(
                    label=key,
                    required=False,
                )
            elif isinstance(value, bool):
                entangled_fields.append(key)
                fields[key] = forms.BooleanField(
                    label=key,
                    required=False,
                )
            elif isinstance(value, decimal.Decimal):
                entangled_fields.append(key)
                fields[key] = forms.DecimalField(
                    label=key,
                    required=False,
                )

        fields["Meta"] = type(
            "Meta",
            (),
            {
                "model": FormEntry,
                "exclude": None,
                "entangled_fields": {"entry_data": entangled_fields},
                "untangled_fields": [
                    "form_name",
                    "form_user",
                ],
            },
        )
        return type("DynamicFormEntryForm", (EntangledModelForm,), fields)

    def get_admin_fieldsets(self):
        return (
            (
                None,
                {
                    "fields": (("form_name", "form_user"),),
                },
            ),
            (
                _("User-entered data"),
                {
                    "fields": tuple(
                        key
                        for key, value in self.entry_data.items()
                        if isinstance(value, (str, tuple, list, bool))
                    )
                },
            ),
        )

    def __str__(self):
        return f"{self.form_name} ({self.pk})"
