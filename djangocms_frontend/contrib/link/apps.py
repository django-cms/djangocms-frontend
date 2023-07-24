from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LinkConfig(AppConfig):
    name = "djangocms_frontend.contrib.link"
    verbose_name = _("Link")

    def ready(self):
        from .helpers import (
            ensure_select2_url_is_available,  # Only import after apps are ready
        )
        ensure_select2_url_is_available()
