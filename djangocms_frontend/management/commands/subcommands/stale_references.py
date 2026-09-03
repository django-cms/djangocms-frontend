from djangocms_frontend import models
from djangocms_frontend.helpers import get_related_object

from .base import SubcommandsCommand


class StaleReferences(SubcommandsCommand):
    help = "Prints all stale references in the djangocms frontend plugins"
    command_name = "stale_references"

    def handle(self, *args, **options):
        for ui_item in models.FrontendUIItem.objects.all().select_related("placeholder"):
            for key, value in ui_item.config.items():
                if isinstance(value, dict) and "model" in value and "pk" in value:
                    if get_related_object(ui_item.config, key) is not None:
                        continue
                    self.stdout.write(self.style.ERROR(f"{ui_item.ui_item} (pk={ui_item.pk}) stale field {key}."))
                    self.stdout.write(self.style.WARNING(f"... {self.get_location(ui_item)}"))

        self.stdout.write(self.style.SUCCESS("Finished checking references"))

    def get_location(self, ui_item):
        """Describes where a plugin lives: its placeholder's source object (page content,
        alias content, ...) if it has one, otherwise the placeholder itself."""
        placeholder = ui_item.placeholder
        if placeholder is None:
            return "not in any placeholder (orphaned plugin)"
        # ``source`` only exists on django CMS 4+; it is None for unattached placeholders
        source = getattr(placeholder, "source", None)
        if source is not None:
            return f'in {source} (placeholder "{placeholder.slot}")'
        return f"in placeholder #{placeholder.pk}"
