from django.conf import settings
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import coerce_decimal

try:
    """Soft dependency on django-captcha for reCaptchaField"""

    from captcha.fields import ReCaptchaField  # NOQA
    from captcha.widgets import (  # NOQA
        ReCaptchaV2Checkbox,
        ReCaptchaV2Invisible,
        ReCaptchaV3,
    )

    installed = True

except ImportError:
    ReCaptchaV2Invisible = forms.HiddenInput  # NOQA
    ReCaptchaV2Checkbox = forms.HiddenInput  # NOQA
    ReCaptchaV3 = forms.HiddenInput  # NOQA
    installed = False

    class ReCaptchaField:  # NOQA
        def __init__(self, *args, **kwargs):
            pass


WIDGETS = {
    "v2-checkbox": ReCaptchaV2Checkbox,
    "v2-invisible": ReCaptchaV2Invisible,
    "v3": ReCaptchaV3,
}


RECAPTCHA_CHOICES = (
    ("v2-checkbox", _("v2 checkbox")),
    ("v2-invisible", _("v2 invisible")),
    ("v3", _("v3")),
)


def get_recaptcha_field(config):
    widget_params = {
        "attrs": {
            key: value
            for key, value in config.get("captcha_config", {}).items()
            if key.startswith("data-")
        },
        "api_params": {
            key: value
            for key, value in config.get("captcha_config", {}).items()
            if not key.startswith("data-")
        },
    }
    widget_params["attrs"]["no_field_sep"] = True
    if config.get("captcha_widget", "") == "v3":
        widget_params["attrs"]["required_score"] = coerce_decimal(
            config.get("captcha_requirement", 0.5)
        )
    field = ReCaptchaField(
        widget=WIDGETS[config.get("captcha_widget", "v2-invisible")](
            **widget_params,
        ),
    )
    return field


installed = installed and (
    hasattr(settings, "RECAPTCHA_PUBLIC_KEY")
    and hasattr(settings, "RECAPTCHA_PRIVATE_KEY")
    or True
)
