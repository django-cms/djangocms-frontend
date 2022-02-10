import json

from django.conf import settings
from django.utils.translation import gettext as _

DEVICE_CHOICES = (
    ("xs", _("Small")),  # default <576px
    ("md", _("Medium")),  # default ≥768px
    ("xl", _("Large")),  # default ≥992px
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


grid_sizes = json.dumps(
    [
        _("Small"),
        _("Medium"),
        _("Large"),
    ]
)

grid_icons = json.dumps(
    [
        "size-xs",
        "size-md",
        "size-xl",
    ]
)


FRAMEWORK_PLUGIN_INFO = {
    "GridRow": {
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "row_links": json.dumps(
            [
                "https://get.foundation/sites/docs/xy-grid.html#block-grids",
            ]
        ),
    },
    "GridColumn": {
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "excl_col_prop": ["xs_me", "xs_ms", "md_me", "md_ms", "xl_me", "xl_ms"],
        "row_links": [
            "https://get.foundation/sites/docs/xy-grid.html#basics",
            "https://get.foundation/sites/docs/flexbox-utilities.html#source-ordering",
            "https://get.foundation/sites/docs/xy-grid.html#offsets",
            "#",
            "#",
        ],
    },
    "CardLayout": {
        "grid_sizes": grid_sizes,
        "grid_icons": grid_icons,
        "row_links": [
            "https://get.foundation/sites/docs/xy-grid.html#block-grids",
        ],
    },
    "Card": {
        "excl_card_prop": [
            "card_context",
            "card_alignment",
            "card_text_color",
            "card_full_height",
            "card_outline",
            "inner_context",
            "text_alignment",
        ],
    },
}


def convert_context(context):
    return context if context != "danger" else "alert"
