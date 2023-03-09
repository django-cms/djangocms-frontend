from django.conf import settings

ICON_CDN = {
    "bootstrap-icons": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css",
    "font-awesome": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "fomantic-ui": "fomantic-ui-icons.css",
}

ICON_LIBRARIES = getattr(settings, "DJANGOCMS_ICON_LIBRARIES", {
    library: (f"{library}.min.json", ICON_CDN.get(library, f"{library}.css")) for library in getattr(
        settings, "DJANGOCMS_ICON_SELECTION",
            (
                "bootstrap-icons", "fomantic-ui", "foundation-icons",
                "font-awesome"
            )
    )
})

ICON_LIBRARIES_JSON = [value[0] for value in ICON_LIBRARIES.values()]
ICON_LIBRARIES_CSS = [value[1] for value in ICON_LIBRARIES.values()]
