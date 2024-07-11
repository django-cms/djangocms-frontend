from django.conf import settings
from django.utils.translation import gettext_lazy as _

DEVICE_CHOICES = (
    ("xs", _("Extra small")),  # default <576px
    ("sm", _("Small")),  # default ≥576px
    ("md", _("Medium")),  # default ≥768px
    ("lg", _("Large")),  # default ≥992px
    ("xl", _("Extra large")),  # default ≥1200px
    ("xxl", _("Extra-extra large")),  # default ≥1200px
)
DEVICE_SIZES = tuple(size for size, name in DEVICE_CHOICES)

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

SPACER_PROPERTY_CHOICES = (
    ("m", "margin"),
    ("p", "padding"),
)

SPACER_SIDE_CHOICES = (
    ("", "*"),
    ("t", "*-top"),
    ("r", "*-right"),
    ("b", "*-bottom"),
    ("l", "*-left"),
    ("x", "*-left & *-right"),
    ("y", "*-top & *-bottom"),
)

SPACER_X_SIDES_CHOICES = (
    ("x", _("Both")),
    ("s", _("Left")),
    ("e", _("Right")),
)

SPACER_Y_SIDES_CHOICES = (
    ("y", _("Both")),
    ("t", _("Top")),
    ("b", _("Bottom")),
)

SPACER_SIZE_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_SPACER_SIZES",
    (
        ("0", "* 0"),
        ("1", "* .25"),
        ("2", "* .5"),
        ("3", "* 1"),
        ("4", "* 1.5"),
        ("5", "* 3"),
    ),
)

SIZE_X_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_SIZE_X_CHOICES",
    (
        ("25", "25%"),
        ("50", "50%"),
        ("75", "75%"),
        ("100", "100%"),
        ("auto", _("Auto")),
        ("vw-100", _("Screen")),
    ),
)

SIZE_Y_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_SIZE_Y_CHOICES",
    (
        ("25", "25%"),
        ("50", "50%"),
        ("75", "75%"),
        ("100", "100%"),
        ("auto", _("Auto")),
        ("min-vh-100", _("Screen (minimum)")),
    ),
)

NAVBAR_DESIGNS = ()
