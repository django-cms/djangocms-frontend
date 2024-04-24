from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LinkConfig(AppConfig):
    name = "djangocms_frontend.contrib.link"
    verbose_name = _("Link")
