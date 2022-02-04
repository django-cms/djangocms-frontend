from djangocms_bootstrap4.constants import DEVICE_SIZES


def breakpoints(props):
    lst = []
    for size in DEVICE_SIZES:
        for prop in props:
            lst.append(f"{size}_{prop}")
    return lst


plugin_migrations = {
    "bootstrap4_alerts.Bootstrap4Alerts -> alert.Alert": [
        "alert_context",
        "alert_dismissable -> alert_dismissible",
        "tag_type",
        "attributes",
        "P001",  # additional data migration, see below
    ],
    "bootstrap4_badge.Bootstrap4Badge -> badge.Badge": [
        "badge_text",
        "badge_context",
        "badge_pills",
        "attributes",
        "P001",  # additional data migration, see below
    ],
    "bootstrap4_card.Bootstrap4Card -> card.Card": [
        "card_type",
        "card_context",
        "card_alignment",
        "card_outline",
        "card_text_color",
        "tag_type",
        "attributes",
        "P001",
        "X002",  # Replace v4 card deck
        "A001_card",  # fix alignment
    ],
    "bootstrap4_card.Bootstrap4CardInner -> card.CardInner": [
        "inner_type",
        "tag_type",
        "attributes",
    ],
    # carousel
    "bootstrap4_collapse.Bootstrap4Collapse -> collapse.Collapse": [
        "siblings",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_collapse.Bootstrap4CollapseContainer -> collapse.CollapseContainer": [
        "identifier -> container_identifier",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_collapse.Bootstrap4CollapseTrigger -> collapse.CollapseTrigger": [
        "identifier -> trigger_identifier",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_content.Bootstrap4Blockquote -> content.Blockquote": [
        "quote_content",
        "quote_origin",
        "quote_alignment",
        "attributes",
        "P001",
        "A001_quote",  # fix alignment
    ],
    "bootstrap4_content.Bootstrap4Code -> content.CodeBlock": [
        "code_content",
        "attributes",
        "P001",
    ],
    "bootstrap4_content.Bootstrap4Figure -> content.Figure": [
        "figure_caption",
        "figure_alignment",
        "attributes",
    ],
    "bootstrap4_grid.Bootstrap4GridContainer -> grid.GridContainer": [
        "container_type",
        "attributes",
        "P001",
        "tag_type",
    ],
    "bootstrap4_grid.Bootstrap4GridRow -> grid.GridRow": [
        "horizontal_alignment",
        "vertical_alignment",
        "gutters",
        "attributes",
        "P001",
        "tag_type",
    ],
    "bootstrap4_grid.Bootstrap4GridColumn -> grid.GridColumn": [
        "column_alignment",
        "() -> text_alignment",
        "attributes",
        "P001",
        "G001",  # fill text_alignment from attributes if possible
        "tag_type",
    ]
    + breakpoints(("col", "order", "ml", "mr", "offset")),
    "bootstrap4_jumbotron.Bootstrap4Jumbotron -> jumbotron.Jumbotron": [
        "fluid -> jumbotron_fluid",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_link.Bootstrap4Link -> link.Link": [
        "template",
        "name",
        "external_link",
        "anchor",
        "mailto",
        "phone",
        "link_type",
        "target -> link_target",
        "link_context",
        "link_size",
        "link_outline",
        "link_block",
        "internal_link",
        "icon_left",
        "icon_right",
        "file_link",
        "attributes",
        "P001",
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroup -> listgroup.ListGroup": [
        "list_group_flush",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroupItem -> listgroup.ListGroupItem": [
        "list_context",
        "list_state",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_media.Bootstrap4Media -> media.Media": [
        "tag_type",
        "attributes",
    ],
    "bootstrap4_media.Bootstrap4MediaBody -> media.MediaBody": [
        "tag_type",
        "attributes",
    ],
    "bootstrap4_picture.Bootstrap4Picture -> image.Image": [
        "template",
        "external_picture",
        "width",
        "height",
        "alignment",
        "caption_text",
        "link_url -> external_link",
        "link_target",
        "link_attributes",
        "use_automatic_scaling",
        "use_no_cropping",
        "use_crop",
        "use_upscale",
        "picture_fluid",
        "picture_rounded",
        "picture_thumbnail",
        "link_page -> internal_link",
        "picture",
        "thumbnail_options",
        "use_responsive_image",
        "attributes",
        "P001",
        "A001_picture",  # fix alignment
    ],
    "bootstrap4_tabs.Bootstrap4Tab -> tabs.Tab": [
        "template",
        "tab_type",
        "tab_alignment",
        "tab_index",
        "tab_effect",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_tabs.Bootstrap4TabItem -> tabs.TabItem": [
        "tab_title",
        "tag_type",
        "attributes",
        "P001",
    ],
    "bootstrap4_utilities.Bootstrap4Spacing -> utilities.Spacing": [
        "space_property",
        "space_sides",
        "space_device",
        "space_size",
        "tag_type",
        "attributes",
        "P001",
    ],
}


def p001_left_right_migration(obj, new_obj):
    if "class" in new_obj.attributes:

        def replace(item, old, new):
            if item == old:
                return new
            return item

        def replace_left(item, old, new):
            if item[: len(old)] == old:
                return new + item[len(old) :]
            return item

        classes = new_obj.attributes["class"].split()
        classes = map(lambda x: replace(x, "text-left", "text-start"), classes)
        classes = map(lambda x: replace(x, "text-right", "text-end"), classes)
        classes = map(lambda x: replace(x, "float-left", "float-start"), classes)
        classes = map(lambda x: replace(x, "float-right", "float-end"), classes)
        classes = map(lambda x: replace(x, "border-left", "border-start"), classes)
        classes = map(lambda x: replace(x, "border-right", "border-end"), classes)
        classes = map(lambda x: replace(x, "no-gutter", "g-0"), classes)
        classes = map(lambda x: replace(x, "text-monospace", "font-monospace"), classes)
        classes = map(lambda x: replace(x, "sr-only", "visually-hidden"), classes)
        classes = map(lambda x: replace_left(x, "left-", "start-"), classes)
        classes = map(lambda x: replace_left(x, "right-", "end-"), classes)
        classes = map(lambda x: replace_left(x, "ml-", "ms-"), classes)
        classes = map(lambda x: replace_left(x, "mr-", "me-"), classes)
        classes = map(lambda x: replace_left(x, "pl-", "ps-"), classes)
        classes = map(lambda x: replace_left(x, "pr-", "pe-"), classes)
        new_obj.config["attributes"]["class"] = " ".join(classes)


def x002_replace_card_deck(obj, new_obj):
    if obj.card_type == "card-deck":
        print("* Detected bootstrap v4 card-deck which is not part of bootstrap5")
        print("  Replaced it with Card Layout, grid cards")
        new_obj.config["card_type"] = "row"
    if obj.card_type == "card-deck" or obj.card_type == "card-group":
        new_obj.plugin_type = "CardLayoutPlugin"
        new_obj.ui_item = "CardLayout"
    classes = obj.attributes.get("class", "").split()
    if "h-100" in classes:
        classes.remove("h-100")
        new_obj.config["card_full_height"] = True
        new_obj.config["attributes"]["class"] = " ".join(classes)
    if new_obj.config["card_alignment"] == "text-left":
        new_obj.config["card_alignment"] = "text-start"
    elif new_obj.config["card_alignment"] == "text-right":
        new_obj.config["card_alignment"] = "text-end"


def a001_alignment(obj, new_obj, field):
    if field in new_obj.config and new_obj.config[field]:
        new_obj.config[field].replace("text-left", "start")
        new_obj.config[field].replace("text-center", "center")
        new_obj.config[field].replace("text-right", "end")


def g001_col_text_alignment(obj, new_obj):
    if obj.column_type != "col":
        print(f"Warning: Break column detected - not supported (id={obj.id})")
    classes = new_obj.config["attributes"].get("class", "").split()
    if "text-left" in classes or "text-start" in classes:
        classes.remove("text-left")
        classes.remove("text-start")
        new_obj.config["text_alignment"] = "start"
    if "text-center" in classes:
        classes.remove("text-center")
        new_obj.config["text_alignment"] = "center"
    if "text-right" in classes or "text-end" in classes:
        classes.remove("text-right")
        classes.remove("text-end")
        new_obj.config["text_alignment"] = "end"
    if classes:
        new_obj.config["attributes"]["class"] = " ".join(classes)
    elif "class" in new_obj.config:
        del new_obj.config["class"]


data_migration = {
    "P001": p001_left_right_migration,
    "X002": x002_replace_card_deck,
    "A001_quote": lambda x, y: a001_alignment(x, y, "quote_alignment"),
    "A001_figure": lambda x, y: a001_alignment(x, y, "figure_alignment"),
    "A001_picture": lambda x, y: a001_alignment(x, y, "alignment"),
    "A001_card": lambda x, y: a001_alignment(x, y, "card_alignment"),
    "G001": g001_col_text_alignment,
}
