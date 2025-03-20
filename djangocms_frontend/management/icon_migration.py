from djangocms_frontend import settings


def m002_responsive_mixin(obj, new_obj):
    classes = new_obj.config["attributes"].get("class", "").split()
    if classes:
        display = (
            "block",
            "flex",
        )
        hidden = "none"

        visible = True
        hit = False
        responsive = []

        for device, _ in settings.DEVICE_CHOICES:
            stump = f"d-{device}-" if device != "xs" else "d-"
            if f"{stump}{hidden}" in classes and visible:
                visible = False
                hit = True
                classes.remove(f"{stump}{hidden}")
            for type in display:
                if f"{stump}{type}" in classes and not visible:
                    visible = True
                    hit = True
                    classes.remove(f"{stump}{type}")
            if visible:
                responsive.append(device)
        if hit:
            new_obj.config["responsive_visibility"] = responsive
            if classes:
                new_obj.config["attributes"]["class"] = " ".join(classes)
            else:
                new_obj.config["attributes"].pop("class")
        else:
            new_obj.config["responsive_visibility"] = None


def m003_background_mixin(obj, new_obj):
    classes = new_obj.config["attributes"].get("class", "").split()
    if classes:
        for context, _ in settings.COLOR_STYLE_CHOICES:
            if f"bg-{context}" in classes:
                new_obj.config["background_context"] = context
                classes.remove(f"bg-{context}")
        for cls, key in {
            "shadow-none": "none",
            "shadow-sm": "sm",
            "shadow": "reg",
            "shadow-lg": "lg",
        }.items():
            if cls in classes:
                new_obj.config["background_shadow"] = key
                classes.remove(cls)
        if classes:
            new_obj.config["attributes"]["class"] = " ".join(classes)
        else:
            new_obj.config["attributes"].pop("class")


def i001_icon(obj, new_obj):
    """Convert icons (only works for fontawesome)"""
    classes = obj.icon.split()

    # Translate from fontawesome 5 to fontawesome 6
    if "fas" in classes:
        library = "fa-solid"
        classes.pop(classes.index("fas"))
    elif "far" in obj.icon:
        library = "fa-regular"
        classes.pop(classes.index("far"))
    elif "fab" in obj.icon:
        library = "fa-brands"
        classes.pop(classes.index("fab"))
    else:
        # Not recognized. Keep classes. Icon, however, probably not visible in the admin.
        new_obj.config["icon"] = {
            "iconClass": obj.icon,
        }
        return

    new_obj.config["icon"] = {
        "libraryId": library,
        "libraryName": "fontAwesome",
        "iconHtml": f'<i class="{library} {" ".join(classes)}"></i>',
        "iconMarkup": "&",
        "iconClass": f"{library} {' '.join(classes)}",
        "iconText": "",
        "library": "font-awesome",
    }


def m001_spacing_mixin(obj, new_obj, type):
    classes = new_obj.config["attributes"].get("class", "").split()
    if classes:
        for size, _ in list(settings.SPACER_SIZE_CHOICES) + ([("auto", "auto")] if type == "margin" else []):
            if f"{type[0]}-{size}" in classes:
                classes.remove(f"{type[0]}-{size}")
                classes.append(f"{type[0]}x-{size}")
                classes.append(f"{type[0]}y-{size}")
            for side, _ in settings.SPACER_X_SIDES_CHOICES:
                if f"{type[0]}{side}-{size}" in classes and not new_obj.config.get(f"{type}_x", None):
                    new_obj.config[f"{type}_x"] = f"{type[0]}{side}-{size}"
                    new_obj.config[f"{type}_devices"] = None
                    classes.remove(f"{type[0]}{side}-{size}")
            for side, _ in settings.SPACER_Y_SIDES_CHOICES:
                if f"{type[0]}{side}-{size}" in classes and not new_obj.config.get(f"{type}_y", None):
                    new_obj.config[f"{type}_y"] = f"{type[0]}{side}-{size}"
                    new_obj.config[f"{type}_devices"] = None
                    classes.remove(f"{type[0]}{side}-{size}")
        if classes:
            new_obj.config["attributes"]["class"] = " ".join(classes)
        else:
            new_obj.config["attributes"].pop("class")


plugin_migration = {
    "djangocms_icon.Icon -> icon.Icon": [
        "attributes",
        "I001_ICON",
        "M001-m",
        "M001-p",
        "M002",
        "M003",
    ],
}
data_migration = {
    "I001_ICON": i001_icon,
    "M001-m": lambda x, y: m001_spacing_mixin(x, y, "margin"),
    "M001-p": lambda x, y: m001_spacing_mixin(x, y, "padding"),
    "M002": m002_responsive_mixin,
    "M003": m003_background_mixin,
}

plugin_prefix = "djangocms_icon"
