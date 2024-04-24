from django.contrib.contenttypes.models import ContentType

plugin_migrations = {
    "djangocms_styledlink.StyledLink -> link.Link": [
        "(default) -> template",
        "label -> name",
        "title",
        "ext_destination -> external_link",
        "ext_follow",
        "mailto",
        "target -> link_target",
        "page_destination -> anchor",
        "() -> phone",
        "() -> link_context",
        "() -> link_size",
        "() -> link_outline",
        "() -> link_block",
        "() -> icon_left",
        "() -> icon_right",
        "() -> file_link",
        "S001",
    ],
    "cms_plugins.ImageContainerModel -> grid.GridContainer": [
        "image -> container_image",
        "(container-fluid) -> container_type",
        "positioning",
        "S002",
    ],
}


def s001_migrate_styled_link(obj, new_obj):
    if obj.int_destination_type_id:
        content_type = ContentType.objects.get(id=obj.int_destination_type_id)
        new_obj.config["internal_link"] = dict(
            model=f"{content_type.app_label}.{content_type.model}",
            pk=obj.int_destination_id,
        )
        styles = obj.styles.all()
        new_obj.config["attributes"] = {"class": " ".join(style.link_class for style in styles)}
        for style in styles:
            obj.styles.remove(style)
        new_obj.config["link_type"] = "btn" if "btn" in new_obj.attributes["class"] else "link"


def s002_migrate_image_container(obj, new_obj):
    new_obj.config["attributes"] = {}
    if obj.additional_classes:
        new_obj.config["attributes"]["class"] = obj.additional_classes
    if obj.additional_styles:
        new_obj.config["attributes"]["style"] = obj.additional_styles

    if "rgba(" in obj.color:
        _, color = obj.color.replace(" ", "").replace(")", "").split("(", 1)
        colors = color.split(",")
        colors[-1].replace(")", "")
        try:
            r, g, b, a = map(float, colors)
            new_obj.config["container_opaqueness"] = int(100 * a)
            if r > 250 and g > 250 and b > 250:
                new_obj.config["container_context"] = "light"
            if r < 5 and g < 5 and b < 5:
                new_obj.config["container_context"] = "dark"
        except (TypeError, AttributeError, ValueError):
            print("Could not convert color", obj.color)
    if obj.blur:
        if "px" in obj.blur:
            try:
                blur = int(obj.blur.replace("px", ""))
                new_obj.config["container_blur"] = blur
            except TypeError:
                print("Could not convert blur", obj.blur)
    if obj.positioning:
        items = obj.positioning.split(";")
        key, value = items[0].split(":", 1)
        new_obj.config["image_position"] = " ".join(value.split()[:2])


data_migration = {
    "S001": s001_migrate_styled_link,
    "S002": s002_migrate_image_container,
}

plugin_prefix = "StyledLink"
