from django.conf import settings as django_setting
from djangocms_bootstrap4.constants import DEVICE_SIZES

from djangocms_frontend import settings


def breakpoints(props):
    lst = []
    for size in DEVICE_SIZES:
        for prop in props:
            if prop == "ml":
                lst.append(f"{size}_ml -> {size}_ms")
            elif prop == "mr":
                lst.append(f"{size}_mr -> {size}_me")
            else:
                lst.append(f"{size}_{prop}")
    return lst


plugin_names = {
    "CodeBlock": "CodePlugin",
}


plugin_migrations = {
    "bootstrap4_alerts.Bootstrap4Alerts -> alert.Alert": [
        "alert_context",
        "alert_dismissable -> alert_dismissible",
        "tag_type",
        "attributes",
        "P001",  # additional data migration, see below
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
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
        "card_context -> background_context",
        "card_alignment",
        "card_outline",
        "card_text_color",
        "tag_type",
        "attributes",
        "P001",
        "X002",  # Replace v4 card deck
        "X003",  # Align card_outline and background_context
        "A001_card",  # fix alignment
        "M001-m",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_card.Bootstrap4CardInner -> card.CardInner": [
        "inner_type",
        "tag_type",
        "attributes",
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    # collapse
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
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_content.Bootstrap4Code -> content.CodeBlock": [
        "code_content",
        "tag_type -> code_type",
        "attributes",
        "P001",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_content.Bootstrap4Figure -> content.Figure": [
        "figure_caption",
        "figure_alignment",
        "attributes",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_grid.Bootstrap4GridContainer -> grid.GridContainer": [
        "container_type",
        "attributes",
        "P001",
        "tag_type",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_grid.Bootstrap4GridRow -> grid.GridRow": [
        "horizontal_alignment",
        "vertical_alignment",
        "gutters",
        "attributes",
        "P001",
        "tag_type",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ],
    "bootstrap4_grid.Bootstrap4GridColumn -> grid.GridColumn": [
        "column_alignment",
        "() -> text_alignment",
        "attributes",
        "P001",
        "G001",  # fill text_alignment from attributes if possible
        "tag_type",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
    ]
    + breakpoints(("col", "order", "ml", "mr", "offset")),
    "bootstrap4_jumbotron.Bootstrap4Jumbotron -> jumbotron.Jumbotron": [
        "fluid -> jumbotron_fluid",
        "(default) -> template",
        "() -> jumbotron_context",
        "() -> jumbotron_opacity",
        "tag_type",
        "attributes",
        "P001",
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "M002",  # ResponsiveMixin
        "M003",  # BackgroundMixin
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
        "M001-m",  # SpacingMixin
        "M001-p",  # SpacingMixin
        "T001_LINK",
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroup -> listgroup.ListGroup": [
        "list_group_flush",
        "tag_type",
        "attributes",
        "P001",
        "M001-m",  # SpacingMixin
        "M002",  # ResponsiveMixin
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroupItem -> listgroup.ListGroupItem": [
        "list_context",
        "list_state",
        "tag_type",
        "attributes",
        "P001",
        "M001-p",  # SpacingMixin
    ],
    "bootstrap4_media.Bootstrap4Media -> media.Media": [
        "tag_type",
        "attributes",
        "M002",  # ResponsiveMixin
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
        "M001-m",  # MarginMixin
        "M002",  # ResponsiveMixin
        "T001_PICTURE",
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
        "T001_TABS",
    ],
    "bootstrap4_tabs.Bootstrap4TabItem -> tabs.TabItem": [
        "tab_title",
        "tag_type",
        "attributes",
        "P001",
        "M001-p",  # SpacingMixin
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
    "bootstrap4_carousel.Bootstrap4Carousel -> carousel.Carousel": [
        "template",
        "carousel_interval",
        "carousel_controls",
        "carousel_indicators",
        "carousel_keyboard",
        "carousel_pause",
        "carousel_ride",
        "carousel_wrap",
        "carousel_aspect_ratio",
        "tag_type",
        "attributes",
        "P001",
        "T001_CAROUSEL",
    ],
    "bootstrap4_carousel.Bootstrap4CarouselSlide -> carousel.CarouselSlide": [
        "template",
        "carousel_image",
        "carousel_content",
        "external_link",
        "target",
        "internal_link",
        "file_link",
        "tag_type",
        "attributes",
        "P001",
        "T001_CAROUSEL_SLIDE",
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
        print("=> Detected bootstrap v4 card-deck which is not part of bootstrap5")
        print("   Replaced it with Card Layout, grid cards")
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


def x003_card_context(obj, new_obj):
    if obj.card_outline:
        new_obj.config["card_outline"] = new_obj.config["background_context"]
        new_obj.config["background_context"] = ""
    else:
        new_obj.config["card_outline"] = ""


def a001_alignment(obj, new_obj, field):
    if field in new_obj.config and new_obj.config[field]:
        new_obj.config[field].replace("text-left", "start")
        new_obj.config[field].replace("text-center", "center")
        new_obj.config[field].replace("text-right", "end")


def m001_spacing_mixin(obj, new_obj, type):  # noqa: A002
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
            for type in display:  # noqa: A001
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
    if "text-end" in classes:
        classes.remove("text-end")
        new_obj.config["text_alignment"] = "end"
    if "text-right" in classes:
        classes.remove("text-right")
        new_obj.config["text_alignment"] = "end"
    if classes:
        new_obj.config["attributes"]["class"] = " ".join(classes)
    elif "class" in new_obj.config["attributes"]:
        new_obj.config["attributes"].pop("class")


def in_choices(choice, choices):
    for key, value in choices:
        if isinstance(value, (tuple, list)):
            if in_choices(choice, value):
                return True
        else:
            if key == choice:
                return True
    return False


def t001_template(obj, new_obj, bs4_setting, dcf_setting):
    if obj.template == "default":
        return
    BS4 = getattr(django_setting, bs4_setting, ())
    DCF = getattr(django_setting, dcf_setting, ())
    if not in_choices(obj.template, BS4):
        print(f"=> Template '{obj.template}' in {obj.plugin_type} (id: {obj.id})")
        print(f"   but not declared in {bs4_setting}")
        print("   You will be able to edit the plugin but up saving the template will be changed.")
        if not DCF and bs4_setting != dcf_setting:
            print(f"   Remember to put {dcf_setting} in your settings.py")


data_migration = {
    "P001": p001_left_right_migration,
    "X002": x002_replace_card_deck,
    "X003": x003_card_context,
    "A001_quote": lambda x, y: a001_alignment(x, y, "quote_alignment"),
    "A001_figure": lambda x, y: a001_alignment(x, y, "figure_alignment"),
    "A001_picture": lambda x, y: a001_alignment(x, y, "alignment"),
    "A001_card": lambda x, y: a001_alignment(x, y, "card_alignment"),
    "G001": g001_col_text_alignment,
    "M001-m": lambda x, y: m001_spacing_mixin(x, y, "margin"),
    "M001-p": lambda x, y: m001_spacing_mixin(x, y, "padding"),
    "M002": m002_responsive_mixin,
    "M003": m003_background_mixin,
    "T001_PICTURE": lambda x, y: t001_template(x, y, "DJANGOCMS_PICTURE_TEMPLATES", "DJANGOCMS_PICTURE_TEMPLATES"),
    "T001_LINK": lambda x, y: t001_template(
        x, y, "DJANGOCMS_LINK_TEMPLATES", "DJANGOCMS_FRONTEND_LINK_TEMPLATE_CHOICES"
    ),
    "T001_TABS": lambda x, y: t001_template(
        x, y, "DJANGOCMS_BOOTSTRAP4_TAB_TEMPLATES", "DJANGOCMS_FRONTEND_TAB_TEMPLATES"
    ),
    "T001_CAROUSEL": lambda x, y: t001_template(
        x,
        y,
        "DJANGOCMS_BOOTSTRAP4_CAROUSEL_TEMPLATES",
        "DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES",
    ),
    "T001_CAROUSEL_SLIDE": lambda x, y: t001_template(
        x,
        y,
        "DJANGOCMS_BOOTSTRAP4_CAROUSEL_TEMPLATES",
        "DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES",
    ),
}

plugin_prefix = "Bootstrap4"
