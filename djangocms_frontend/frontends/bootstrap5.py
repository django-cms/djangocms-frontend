import json

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
DEVICE_SIZES = tuple([size for size, name in DEVICE_CHOICES])

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

FRAMEWORK_PLUGIN_INFO = {
    "GridColumn": {
        "row_links": json.dumps(
            [
                "https://getbootstrap.com/docs/5.1/layout/grid/#grid-options",
                "https://getbootstrap.com/docs/5.1/layout/columns/#reordering",
                "https://getbootstrap.com/docs/5.1/layout/columns/#offsetting-columns",
                "https://getbootstrap.com/docs/5.1/utilities/flex/#auto-margins",
                "https://getbootstrap.com/docs/5.1/utilities/flex/#auto-margins",
            ]
        ),
    },
    "GridRow": {
        "row_links": json.dumps(
            [
                "https://getbootstrap.com/docs/5.1/layout/grid/#row-columns",
            ]
        ),
        "vertical_alignment_link": "https://getbootstrap.com/docs/5.1/layout/columns/#vertical-alignment",
        "horizontal_alignment_link": "https://getbootstrap.com/docs/5.1/layout/columns/#horizontal-alignment",
    },
    "CardLayout": {
        "card_type_link": "https://getbootstrap.com/docs/5.1/components/card/#card-layout",
        "row_links": json.dumps(
            [
                "https://getbootstrap.com/docs/5.1/layout/grid/#row-columns",
            ]
        ),
    },
}
