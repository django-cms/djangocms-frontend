from django.conf import settings
from django.utils.translation import gettext_lazy as _

VENDOR_PATH = "djangocms_frontend/icon/vendor/assets"

ICON_CDN = {
    "bootstrap-icons": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.4/font/bootstrap-icons.css",
    "font-awesome": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "material-icons-filled": "https://fonts.googleapis.com/css2?family=Material+Icons",
    "material-icons-outlined": "https://fonts.googleapis.com/css2?family=Material+Icons+Outlined",
    "material-icons-round": "https://fonts.googleapis.com/css2?family=Material+Icons+Round",
    "material-icons-sharp": "https://fonts.googleapis.com/css2?family=Material+Icons+Sharp",
    "material-icons-two-tone": "https://fonts.googleapis.com/css2?family=Material+Icons+Two+Tone",
    "fomantic-ui": "fomantic-ui-icons.css",
}

ICON_LIBRARIES_SHOWN = getattr(
    settings,
    "DJANGOCMS_FRONTEND_ICONS_LIBRARIES_SHOWN",
    (
        "font-awesome",
        "bootstrap-icons",
        "material-icons-filled",
        "material-icons-outlined",
        "material-icons-round",
        "material-icons-sharp",
        "material-icons-two-tone",
        "fomantic-ui",
        "foundation-icons",
        "elegant-icons",
        "feather-icons",
        "open-iconic",
        "tabler-icons",
        "weather-icons",
    ),
)

ICON_LIBRARIES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_ICON_LIBRARIES",
    {
        library: (f"{library}.min.json", ICON_CDN.get(library, f"{library}.css"))
        for library in getattr(settings, "DJANGOCMS_FRONTEND_ICON_LIBRARIES_SHOWN", ICON_LIBRARIES_SHOWN)
    },
)

ICON_SIZE_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_ICON_SIZE_CHOICES",
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

ICON_TAG_TYPES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_ICON_TAG_TYPES",
    ("i", "span"),
)

ICON_TAG_TYPES = tuple((entry, entry) for entry in ICON_TAG_TYPES)
