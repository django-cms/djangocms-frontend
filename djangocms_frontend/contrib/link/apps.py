from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.urls import NoReverseMatch, clear_url_caches, include, path, reverse
from django.utils.translation import gettext_lazy as _


class LinkConfig(AppConfig):
    name = "djangocms_frontend.contrib.link"
    verbose_name = _("Link")

    def ready(self):
        """Install the URLs"""
        try:
            reverse("dcf_autocomplete:ac_view")
        except NoReverseMatch:  # Not installed yet
            urlconf_module = import_module(settings.ROOT_URLCONF)
            urlconf_module.urlpatterns = [
                path(
                    "@dcf-frontend_link/",
                    include(
                        "djangocms_frontend.contrib.link.urls",
                        namespace="dcf_autocomplete",
                    ),
                )
            ] + urlconf_module.urlpatterns
            clear_url_caches()
