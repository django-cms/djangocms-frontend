from django.apps import apps

from .base import SubcommandsCommand


class ClearAdvancedSettings(SubcommandsCommand):
    help = "Clears all advanced settings (attributes and tag_type) from djangocms-frontend plugins"
    command_name = "clear_advanced_settings"

    def handle(self, *args, **options):
        if options["interactive"]:
            self.stdout.write(
                "This command clears all advanced settings (custom attributes and tag_type) "
                "from all djangocms-frontend plugins.\n"
                "Changes cannot be undone. Are you sure you want to proceed?\n"
            )
            ok = input("Type 'yes' to continue, or 'no' to cancel: ")
        else:
            ok = "yes"

        if ok != "yes":
            self.stdout.write(self.style.ERROR("Aborted."))
            return

        from djangocms_frontend.models import AbstractFrontendUIItem

        default_tag_type = AbstractFrontendUIItem._meta.get_field("tag_type").default
        dcf_models = [m for m in apps.get_models() if issubclass(m, AbstractFrontendUIItem) and not m._meta.abstract]

        total_attributes_cleared = 0
        total_tag_type_reset = 0

        for model in dcf_models:
            # Bulk-reset tag_type for all instances with non-default values
            total_tag_type_reset += model.objects.exclude(tag_type=default_tag_type).update(tag_type=default_tag_type)
            # Attributes are stored in config JSON, so we need per-object handling;
            # use iterator() to avoid loading all instances into memory at once
            for obj in model.objects.iterator():
                if obj.config.get("attributes"):
                    obj.config["attributes"] = {}
                    obj.save()
                    total_attributes_cleared += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Cleared attributes on {total_attributes_cleared} plugin(s), "
                f"reset tag_type on {total_tag_type_reset} plugin(s)."
            )
        )
