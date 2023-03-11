from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IconConfig(AppConfig):
    name = "djangocms_frontend.contrib.icon"
    verbose_name = _("Icon")
