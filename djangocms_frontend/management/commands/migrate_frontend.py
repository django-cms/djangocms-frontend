from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, models

from djangocms_frontend.settings import DEVICE_SIZES


def breakpoints(props):
    lst = []
    for size in DEVICE_SIZES:
        for prop in props:
            lst.append(f"{size}_{prop}")
    return lst


plugin_names = {
    "Picture": "ImagePlugin",
}

plugin_migrations = {
    "bootstrap4_alerts.Bootstrap4Alerts -> alert.Alert": [
        "alert_context",
        "alert_dismissable -> alert_dismissible",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_badge.Bootstrap4Badge -> badge.Badge": [
        "badge_text",
        "badge_context",
        "badge_pills",
        "attributes",
    ],
    "bootstrap4_card.Bootstrap4Card -> card.Card": [
        "card_type",
        "card_context",
        "card_alignment",
        "card_outline",
        "card_text_color",
        "tag_type",
        "attributes",
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
    ],
    "bootstrap4_content.Bootstrap4Blockquote -> content.Blockquote": [
        "quote_content",
        "quote_origin",
        "quote_alignment",
        "attributes",
    ],
    "bootstrap4_content.Bootstrap4Code -> content.CodeBlock": [
        "code_content",
        "attributes",
    ],
    "bootstrap4_content.Bootstrap4Figure -> content.Figure": [
        "figure_caption",
        "figure_alignment",
        "attributes",
    ],
    "bootstrap4_grid.Bootstrap4GridContainer -> grid.GridContainer": [
        "container_type",
        "attributes",
        "tag_type",
    ],
    "bootstrap4_grid.Bootstrap4GridRow -> grid.GridRow": [
        "horizontal_alignment",
        "vertical_alignment",
        "gutters",
        "attributes",
        "tag_type",
    ],
    "bootstrap4_grid.Bootstrap4GridColumn -> grid.GridColumn": [
        "column_type",
        "column_alignment",
        "attributes",
        "tag_type",
    ]
    + breakpoints(("col", "order", "ml", "mr", "offset")),
    "bootstrap4_jumbotron.Bootstrap4Jumbotron -> jumbotron.Jumbotron": [
        "fluid -> jumbotron_fluid",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_link.Bootstrap4Link -> link.Link": [
        "template",
        "name",
        "external_link",
        "anchor",
        "mailto",
        "phone",
        "target -> link_target",
        "link_type",
        "link_context",
        "link_size",
        "link_outline",
        "link_block",
        "internal_link",
        "icon_left",
        "icon_right",
        "file_link",
        "attributes",
    ],
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
        "X001",
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroup -> listgroup.ListGroup": [
        "list_group_flush",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_listgroup.Bootstrap4ListGroupItem -> listgroup.ListGroupItem": [
        "list_context",
        "list_state",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_media.Bootstrap4Media -> media.Media": [
        "tag_type",
        "attributes",
    ],
    "bootstrap4_media.Bootstrap4MediaBody -> media.MediaBody": [
        "tag_type",
        "attributes",
    ],
    "bootstrap4_picture.Bootstrap4Picture -> picture.Picture": [
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
    ],
    "bootstrap4_tabs.Bootstrap4Tab -> tabs.Tab": [
        "template",
        "tab_type",
        "tab_alignment",
        "tab_index",
        "tab_effect",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_tabs.Bootstrap4TabItem -> tabs.TabItem": [
        "tab_title",
        "tag_type",
        "attributes",
    ],
    "bootstrap4_utilities.Bootstrap4Spacing -> utilities.Spacing": [
        "space_property",
        "space_sides",
        "space_device",
        "space_size",
        "tag_type",
        "attributes",
    ],
}


def migrate_to_djangocms_frontend(apps, schema_editor):
    cnt = 0
    for plugin_model, fields in plugin_migrations.items():
        old, new = plugin_model.split(" -> ")
        old_app, old_model = old.rsplit(".", 1)
        new_app, new_model = new.rsplit(".", 1)
        if old_app in apps.all_models:
            OldPluginModel = apps.get_model(old_app, old_model)
            NewPluginModel = apps.get_model(new_app, new_model)
            for obj in OldPluginModel.objects.all():
                #
                new_obj = NewPluginModel()
                new_obj.id = obj.id
                new_obj.placeholder = obj.placeholder
                new_obj.parent = obj.parent
                new_obj.position = obj.position
                new_obj.language = obj.language
                new_obj.creation_date = obj.creation_date
                new_obj.depth = obj.depth
                new_obj.path = obj.path
                new_obj.numchild = obj.numchild
                new_obj.plugin_type = (
                    plugin_names[new_model]
                    if new_model in plugin_names
                    else new_model + "Plugin"
                )
                # Add something like `new_obj.field_name = obj.field_name` for any field in the the new plugin
                for field in fields:
                    if field == "X001":  # Special case internal link from styled link
                        if obj.int_destination_type_id:
                            content_type = ContentType.objects.get(
                                id=obj.int_destination_type_id
                            )
                            new_obj.config["internal_link"] = dict(
                                model=f"{content_type.app_label}.{content_type.model}",
                                pk=obj.int_destination_id,
                            )
                            styles = obj.styles.all()
                            new_obj.config["attributes"] = {
                                "class": " ".join(
                                    (style.link_class for style in styles)
                                )
                            }
                            for style in styles:
                                obj.styles.remove(style)
                            new_obj.config["link_type"] = (
                                "btn"
                                if "btn" in new_obj.attributes["class"]
                                else "link"
                            )
                    else:
                        if " -> " in field:
                            old_field, new_field = field.split(" -> ")
                        else:
                            old_field, new_field = field, field
                        value = (
                            old_field[1:-1]
                            if old_field[0] == "("
                            else getattr(obj, old_field)
                        )
                        if value == "":
                            value = None
                        if hasattr(new_obj, new_field):
                            setattr(new_obj, new_field, value)
                        else:
                            if isinstance(value, models.Model):  # related field
                                if (
                                    new_field == "internal_link" and False
                                ):  # link convention
                                    type_class = ContentType.objects.get_for_model(
                                        value.__class__
                                    )
                                    value = f"{type_class.id}-{value.id}"
                                else:  # django-entangled convention
                                    value = {
                                        "model": "{}.{}".format(
                                            value._meta.app_label,
                                            value._meta.model_name,
                                        ),
                                        "pk": value.pk,
                                    }
                            elif isinstance(
                                value, models.QuerySet
                            ):  # related many field
                                value = {
                                    "model": "{}.{}".format(
                                        value.model._meta.app_label,
                                        value.model._meta.model_name,
                                    ),
                                    "p_keys": list(value.values_list("pk", flat=True)),
                                }
                            new_obj.config[new_field] = value

                new_obj.save()
                # Now delete old plugin from its table w/o checking for child plugins
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"DELETE FROM `{obj._meta.db_table}` WHERE cmsplugin_ptr_id={obj.id};"
                    )
                cnt += 1
                print(f"{cnt:7}", end="\r")
                # Copy any many to many field after save:`new_plugin.many2many.set(old_plugin.many2many.all())`
        else:
            print(f"{old_app} not installed.")
    print()


class Command(BaseCommand):
    help = "Migrates plugins djangocms_bootstrap4 to djangocms_frontend"

    def handle(self, *args, **options):
        migrate_to_djangocms_frontend(apps, None)
        self.stdout.write(self.style.SUCCESS("Successfully migrated plugins"))
