from django.apps import apps


def i001_icon(obj, new_obj):
    """Convert icons (only works for font awesome)"""
    classes = obj.icon.split()

    if "fas" in classes:
        library = "fa-solid"
        classes.pop(classes.index("fas"))
    elif "far" in obj.icon:
        library = "fa-regular"
        classes.pop(classes.index("far"))
    elif "fab" in obj.icon:
        library = "fa-brand"
        classes.pop(classes.index("fab"))
    else:
        library = obj.icon.split()[0]
        classes.pop(0)

    icon_obj = {
        "libraryId": library,
        "libraryName": "fontAwesome",
        "iconHtml": f'<i class="{library} {" ".join(classes)}"></i>',
        "iconMarkup": "&",
        "iconClass": f'{library} {" ".join(classes)}',
        "iconText": "",
        "library": "font-awesome",
    }
    new_obj.config["icon"] = icon_obj


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
