from django.db.models import Count

from djangocms_frontend.models import FrontendUIItem

from .base import SubcommandsCommand


class FrequencyAnalysis(SubcommandsCommand):
    help = "Migrates plugins djangocms_bootstrap4 to djangocms_frontend"
    command_name = "frequency_analysis"

    def handle(self, *args, **options):
        analysis = FrontendUIItem.objects.values("ui_item").annotate(count=Count("ui_item")).order_by("-count")
        for element in analysis:
            self.stdout.write(f"{element['ui_item']:20}\t{element['count']:6}")
