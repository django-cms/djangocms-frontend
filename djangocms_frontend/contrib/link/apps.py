from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .helpers import ensure_select2_url_is_available


class LinkConfig(AppConfig):
    name = "djangocms_frontend.contrib.link"
    verbose_name = _("Link")

    def ready(self):
        ensure_select2_url_is_available()
