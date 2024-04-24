from djangocms_frontend import models
from djangocms_frontend.helpers import get_related_object

from .base import SubcommandsCommand


class StaleReferences(SubcommandsCommand):
    help = "Prints all stale references in the djangocms frontend plugins"
    command_name = "stale_references"

    def handle(self, *args, **options):
        for ui_item in models.FrontendUIItem.objects.all():
            for key, value in ui_item.config.items():
                if isinstance(value, dict):
                    if "model" in value and "pk" in value:
                        obj = get_related_object(ui_item.config, key)
                        if obj is None:
                            msg = f"{ui_item.ui_item} (pk={ui_item.pk}) stale field {key}."
                            pages = ui_item.placeholder.page_set.all()
                            self.stdout.write(self.style.ERROR(msg))
                            if pages:
                                for page in pages:
                                    self.stdout.write(
                                        self.style.WARNING(f"... on page #{page.id}, at {page.get_absolute_url()}")
                                    )
                            else:
                                self.stdout.write(self.style.WARNING(f"... in placeholder #{ui_item.placeholder.id}"))

        self.stdout.write(self.style.SUCCESS("Finished checking references"))
