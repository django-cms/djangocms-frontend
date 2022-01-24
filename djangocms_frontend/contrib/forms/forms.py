from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.contrib import forms as forms_module
from djangocms_frontend.fields import AttributesFormField, ColoredButtonGroup
from djangocms_frontend.models import FrontendUIItem

mixin_factory = settings.get_forms(forms_module)


class ContactForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    subject = forms.CharField(label=_("Subject"), required=False)
    content = forms.CharField(
        label=_("Content"),
        widget=forms.Textarea(attrs=dict(style="height: 240px;")),
        help_text="Put your message here!",
    )

    #      template = "cmsplugin_contact/contact.html"
    redirect = "/"
    frontend_options = {
        "floating_labels": True,
    }

    fieldsets = (
        (
            "Contact form",
            {
                "floating": True,
                #                          "classes": ("collapse", "show",),
                "fields": (
                    (
                        "email",
                        "subject",
                    ),
                    "content",
                ),
            },
        ),
    )


class FormsForm(mixin_factory("Form"), EntangledModelForm):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "form_submit_message",
                "form_submit_context",
                "form_submit_align",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    form_submit_message = forms.CharField(
        label=_("Submit message"),
        initial=_("Submit"),
        required=True,
    )
    form_submit_context = forms.ChoiceField(
        label=_("Subit Context"),
        choices=settings.COLOR_STYLE_CHOICES,
        initial=settings.COLOR_STYLE_CHOICES[0][0],
        required=True,
        widget=ColoredButtonGroup(),
    )
    form_submit_align = forms.ChoiceField(
        label=_("Submit button alignment"),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
    )
    attributes = AttributesFormField()
