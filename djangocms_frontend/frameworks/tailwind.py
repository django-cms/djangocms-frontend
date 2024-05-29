from django.conf import settings
from django.utils.translation import gettext_lazy as _

COLOR_STYLE_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES",
    (
        ("default", _("Default")),
        ("alternative", _("Alternative")),
        ("green", _("Green")),
        ("red", _("Red")),
        ("yellow", _("Yellow")),
        ("purple", _("Purple")),
        ("light", _("Light")),
        ("dark", _("Dark")),
    ),
)
