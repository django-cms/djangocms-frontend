from django.conf import settings
from django.utils.translation import gettext_lazy as _

ICON_CDN = {
    "bootstrap-icons": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css",
    "font-awesome": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "fomantic-ui": "fomantic-ui-icons.css",
}

ICON_LIBRARIES = getattr(
    settings,
    "DJANGOCMS_ICON_LIBRARIES",
    {
        library: (f"{library}.min.json", ICON_CDN.get(library, f"{library}.css"))
        for library in getattr(
            settings,
            "DJANGOCMS_ICON_SELECTION",
            ("bootstrap-icons", "fomantic-ui", "foundation-icons", "font-awesome"),
        )
    },
)

ICON_LIBRARIES_JSON = [value[0] for value in ICON_LIBRARIES.values()]
ICON_LIBRARIES_CSS = [value[1] for value in ICON_LIBRARIES.values()]

ICON_SIZE_CHOICES = getattr(
    settings,
    "DJANGOCMS_ICON_SIZE_CHOICES",
    (
        ("", _("Regular")),
        ("200%", _("x 2")),
        ("300%", _("x 3")),
        ("400%", _("x 4")),
        ("500%", _("x 5")),
        ("800%", _("x 8")),
        ("1200%", _("x 12")),
    ),
)
