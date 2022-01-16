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
}

def x001_migrate_styled_link(obj, new_obj):
    if obj.int_destination_type_id:
        content_type = ContentType.objects.get(id=obj.int_destination_type_id)
        new_obj.config["internal_link"] = dict(
            model=f"{content_type.app_label}.{content_type.model}",
            pk=obj.int_destination_id,
        )
        styles = obj.styles.all()
        new_obj.config["attributes"] = {
            "class": " ".join((style.link_class for style in styles))
        }
        for style in styles:
            obj.styles.remove(style)
        new_obj.config["link_type"] = (
            "btn" if "btn" in new_obj.attributes["class"] else "link"
        )


data_migration = {
    "S001": x001_migrate_styled_link,
}
