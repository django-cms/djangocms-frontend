from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

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
        ("primary", _("Primary")),
        ("secondary", _("Secondary")),
        ("success", _("Success")),
        ("danger", _("Danger")),
        ("warning", _("Warning")),
        ("info", _("Info")),
        ("light", _("Light")),
        ("dark", _("Dark")),
    ),
)

COLOR_CODES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_COLOR_CODES",
    dict(),
)

FORM_TEMPLATE = getattr(
    settings,
    "DJANGOCMS_FRONTEND_FORM_TEMPLATE",
    "djangocms_frontend/bootstrap5/render/form.html",
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

OPACITY_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_OPACITY_CHOICES",
    (
        (100, "100%"),
        (75, "75%"),
        (50, "50%"),
        (25, "25%"),
        (10, "10%"),
    ),
)

SHADOW_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_SHADOW_CHOICES",
    (
        ("none", pgettext_lazy("shadow", "None")),
        ("sm", "S"),
        ("reg", "M"),
        ("lg", "L"),
    ),
)

grid_sizes = [
    _("Extra small"),
    _("Small"),
    _("Medium"),
    _("Large"),
    _("Extra large"),
    _("XX large"),
]

grid_icons = ["size-xs", "size-sm", "size-md", "size-lg", "size-xl", "size-xxl"]


FRAMEWORK_PLUGIN_INFO = {
    "GridColumn": {
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "row_links": [
            "https://getbootstrap.com/docs/5.1/layout/grid/#grid-options",
            "https://getbootstrap.com/docs/5.1/layout/columns/#reordering",
            "https://getbootstrap.com/docs/5.1/layout/columns/#offsetting-columns",
            "https://getbootstrap.com/docs/5.1/utilities/flex/#auto-margins",
            "https://getbootstrap.com/docs/5.1/utilities/flex/#auto-margins",
        ],
    },
    "GridRow": {
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "row_links": [
            "https://getbootstrap.com/docs/5.1/layout/grid/#row-columns",
        ],
        "vertical_alignment_link": "https://getbootstrap.com/docs/5.1/layout/columns/#vertical-alignment",
        "horizontal_alignment_link": "https://getbootstrap.com/docs/5.1/layout/columns/#horizontal-alignment",
    },
    "CardLayout": {
        "card_type_link": "https://getbootstrap.com/docs/5.1/components/card/#card-layout",
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "row_links": [
            "https://getbootstrap.com/docs/5.1/layout/grid/#row-columns",
        ],
    },
}

NAVBAR_DESIGNS = getattr(
    settings,
    "DJANGOCMS_FRONTEND_NAVBAR_DESIGN",
    (
        ("light", _("Light")),
        ("dark", _("Dark")),
    ),
)
