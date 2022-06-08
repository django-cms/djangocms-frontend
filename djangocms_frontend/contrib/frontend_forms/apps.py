from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.urls import NoReverseMatch, clear_url_caches, include, path, reverse
from django.utils.translation import gettext_lazy as _


class FormsConfig(AppConfig):
    name = "djangocms_frontend.contrib.frontend_forms"
    verbose_name = _("Forms")

    def ready(self):
        """Install the URLs"""

        from django.core.checks import Warning, register

        @register()
        def deprecation_check(app_configs, **kwargs):
            return [
                Warning(
                    "djangocms_frontend.contrib.frontend_forms will be removed in version 1.0",
                    obj=self,
                    hint="Use djangocms-form-builder instead.",
                    id="djangocms_frontend.W001",
                )
            ]

        try:
            reverse("dcf_forms:ajax_form")
        except NoReverseMatch:  # Not installed yet
            urlconf_module = import_module(settings.ROOT_URLCONF)
            urlconf_module.urlpatterns = [
                path(
                    "@dcf-frontend_forms/",
                    include(
                        "djangocms_frontend.contrib.frontend_forms.urls",
                        namespace="dcf_forms",
                    ),
                )
            ] + urlconf_module.urlpatterns
            clear_url_caches()
