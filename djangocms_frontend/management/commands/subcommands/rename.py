from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from django.db import transaction

from djangocms_frontend.models import AbstractFrontendUIItem

from .base import SubcommandsCommand


class Rename(SubcommandsCommand):
    help_string = "Renames a plugin type in the database"
    command_name = "rename"

    def add_arguments(self, parser):
        parser.add_argument("old_plugin", help="The plugin type to rename (must not be installed but present in db)")
        parser.add_argument("new_plugin", help="The plugin type to rename to (must be installed)")

    def handle(self, *args, **options):
        old_plugin = options["old_plugin"]
        new_plugin = options["new_plugin"]

        # Verify old_plugin is not installed
        all_plugins = plugin_pool.get_all_plugins()
        installed_names = {cls.__name__: cls for cls in all_plugins}

        if old_plugin in installed_names:
            self.stderr.write(self.style.ERROR(f"Plugin '{old_plugin}' is still installed. It must not be installed."))
            return

        # Verify old_plugin exists in db
        count = CMSPlugin.objects.filter(plugin_type=old_plugin).count()
        if count == 0:
            self.stderr.write(self.style.ERROR(f"Plugin '{old_plugin}' not found in the database."))
            return

        # Verify new_plugin is installed
        if new_plugin not in installed_names:
            self.stderr.write(self.style.ERROR(f"Plugin '{new_plugin}' is not installed."))
            return

        new_plugin_cls = installed_names[new_plugin]
        has_model = new_plugin_cls.model is not None
        update_ui_item = has_model and issubclass(new_plugin_cls.model, AbstractFrontendUIItem)

        # Warn and require confirmation if new plugin has a model but is not an AbstractFrontendUIItem
        if has_model and not update_ui_item:
            self.stdout.write(
                self.style.WARNING(
                    f"Warning: '{new_plugin}' is not based on AbstractFrontendUIItem. "
                    "No plugin model instances will be created or migrated. "
                    "Only the plugin_type field on CMSPlugin will be updated."
                )
            )
            if options["interactive"]:
                ok = input("Type 'yes' to continue, or 'no' to cancel: ").lower()
            else:
                ok = "yes"
            if ok not in ("yes", "y"):
                self.stdout.write(self.style.ERROR("Aborted."))
                return

        # Update plugin_type and ui_item atomically
        with transaction.atomic():
            updated = CMSPlugin.objects.filter(plugin_type=old_plugin).update(plugin_type=new_plugin)
            self.stdout.write(
                self.style.SUCCESS(f"Updated {updated} plugins: plugin_type '{old_plugin}' -> '{new_plugin}'")
            )

            # Update ui_item if the new plugin's model is a subclass of AbstractFrontendUIItem
            if update_ui_item:
                new_ui_item = new_plugin_cls.model.__name__
                ui_updated = (
                    new_plugin_cls.model.objects.filter(plugin_type=new_plugin)
                    .exclude(ui_item=new_ui_item)
                    .update(ui_item=new_ui_item)
                )
                if ui_updated:
                    self.stdout.write(self.style.SUCCESS(f"Updated {ui_updated} plugins: ui_item -> '{new_ui_item}'"))
