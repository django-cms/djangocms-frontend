from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

"""Soft dependency on django-captcha"""

ReCaptchaV2Invisible = None  # NOQA


class ReCaptchaField:  # NOQA
    def __init__(self, *args, **kwargs):
        pass


if hasattr(settings, "") and hasattr(settings, ""):
    try:
        from captcha.fields import ReCaptchaField  # NOQA
        from captcha.widgets import ReCaptchaV2Invisible  # NOQA
    except ImportError:
        pass


# Honeypot widget -- most automated spam posters will check any checkbox
# assuming it's an "I accept terms and conditions" box
class HoneypotWidget(forms.CheckboxInput):
    is_hidden = True

    def render(self, *args, **kwargs):
        wrapper_html = (
            '<div style="display: none;"><label for="id_accept_terms">%s</label>%%s</div>'
            % (_("Are you a robot?"))
        )
        return mark_safe(
            wrapper_html % super(HoneypotWidget, self).render(*args, **kwargs)
        )


class HoneypotField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super(HoneypotField, self).__init__(
            widget=HoneypotWidget,
            required=False,
            error_messages={"checked": _("Please don't check this box.")},
            *args,
            **kwargs,
        )

    def clean(self, value):
        val = super(HoneypotField, self).clean(value)
        if val:
            raise ValidationError(self.error_messages["checked"])
        return val


class ContactForm(forms.Form):
    class Meta:
        verbose_name = _("Contact form")
        options = {
            "floating_labels": True,
        }
        fieldsets = (
            (
                None,
                {
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

    template = "djangocms_frontend/contact_form_body.txt"
    recipients = settings.ADMINS
    render_success = "djangocms_frontend/contact_form_success.html"
    # replace = True

    email = forms.EmailField(label=_("Email"))
    subject = forms.CharField(label=_("Subject"), required=False)
    content = forms.CharField(
        label=_("Content"),
        widget=forms.Textarea(attrs=dict(style="height: 240px;")),
    )
    honeypot = HoneypotField()
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Invisible,
        public_key=settings.RECAPTCHA_V2_INVISIBLE,
        private_key=settings.RECAPTCHA_V2_SECRET,
    )

    def save(self):
        EmailMessage(
            to=[mail for _, mail in self.recipients],
            subject=f"[{self.__class__.__name__}] {self.cleaned_data['subject']}",
            body=render_to_string(
                self.template,
                dict(
                    email=self.cleaned_data["email"],
                    content=self.cleaned_data["content"],
                ),
            ),
            headers={"Reply-To": self.cleaned_data["email"]},
        ).send()
