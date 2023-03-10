from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.urls import NoReverseMatch, clear_url_caches, include, path, reverse
from django.utils.translation import gettext_lazy as _


class IconConfig(AppConfig):
    name = "djangocms_frontend.contrib.icon"
    verbose_name = _("Icon")
