import djangocms_frontend

from .subcommands.base import SubcommandsCommand
from .subcommands.frequency_analysis import FrequencyAnalysis
from .subcommands.migrate import Migrate
from .subcommands.stale_references import StaleReferences
from .subcommands.sync_permissions import SyncPermissions


class Command(SubcommandsCommand):
    command_name = "frontend"
    subcommands = {
        "migrate": Migrate,
        "frequency_analysis": FrequencyAnalysis,
        "stale_references": StaleReferences,
        "sync_permissions": SyncPermissions,
    }
    missing_args_message = "one of the available sub commands must be provided"

    subcommand_dest = "command"

    def get_version(self):
        return djangocms_frontend.__version__

    def add_arguments(self, parser):
        parser.add_argument("--version", action="version", version=self.get_version())
        super().add_arguments(parser)
