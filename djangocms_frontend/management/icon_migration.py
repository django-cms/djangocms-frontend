def i001_icon(obj, new_obj):
    """Convert icons (only works for font awesome)"""
    classes = obj.icon.split()

    # Translate from fontawesome 5 to fontawsome 6
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
        "iconClass": f'{library} {" ".join(classes)}',
        "iconText": "",
        "library": "font-awesome",
    }


plugin_migration = {
    "djangocms_icon.Icon -> icon.Icon": [
        "icon",
        "M002",
        "M003",
    ],
}
data_migration = {
    "I001_ICON": i001_icon,
}

plugin_prefix = "djangocms_icon"
