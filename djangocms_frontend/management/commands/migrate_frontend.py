from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, models

from djangocms_frontend.management import bootstrap4_migration, styled_link_migration

plugin_names = {}


plugin_migrations = {}
data_migration = {}

# Bootstrap 4
if "djangocms_bootstrap4" in apps.all_models:
    plugin_migrations.update(bootstrap4_migration.plugin_migrations)
    data_migration.update(bootstrap4_migration.data_migration)
# Styled link
if "djangocms_styledlink" in apps.all_models:
    plugin_migrations.update(styled_link_migration.plugin_migrations)
    data_migration.update(styled_link_migration.data_migration)


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
                new_obj_fields = [field.name for field in new_obj._meta.get_fields()]
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
                    if field in data_migration:
                        data_migration[field](obj, new_obj)
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
                        if new_field in new_obj_fields:
                            setattr(new_obj, new_field, value)
                        else:
                            if isinstance(value, models.Model):  # related field
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
