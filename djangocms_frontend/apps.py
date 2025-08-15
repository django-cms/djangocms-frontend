from django import apps
from django.core import checks


class DjangocmsFrontendConfig(apps.AppConfig):
    name = "djangocms_frontend"
    verbose_name = "django CMS Frontend"

    def ready(self):
        from . import component_pool, plugin_tag

        component_pool.setup()
        plugin_tag.setup()
        checks.register(check_settings)
        checks.register(check_installed_apps)


def check_settings(*args, **kwargs):  # pragma: no cover
    from django.conf import settings

    warnings = []

    if hasattr(settings, "DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH"):
        warnings.append(
            checks.Warning(
                "The DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH setting was removed in djangocms-frontend 2.",
                "Use DJANGOCMS_LINK_MINIMUM_INPUT_LENGTH instead.",
                id="djangocms_frontend.W001",
                obj="settings.DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH",
            )
        )
    if hasattr(settings, "DJANGOCMS_FRONTEND_LINK_MODELS"):
        warnings.append(
            checks.Warning(
                "The DJANGOCMS_FRONTEND_LINK_MODELS setting was removed in djangocms-frontend 2. "
                "djangocms-frontend 2 uses linkable models from djangocms-link. See "
                "https://github.com/django-cms/djangocms-link#django-cms-link for more info.",
                "This message disappears after removing the DJANGOCMS_FRONTEND_LINK_MODELS from your "
                "project's settings.\n",
                id="djangocms_frontend.W002",
                obj="settings.DJANGOCMS_FRONTEND_LINK_MODELS",
            )
        )
    return warnings


def check_installed_apps(*args, **kwargs):  # pragma: no cover
    from django.conf import settings

    errors = []
    link_contrib_apps = [
        "djangocms_frontend.contrib.carousel",
        "djangocms_frontend.contrib.image",
        "djangocms_frontend.contrib.link",
    ]
    link_apps_used = [app for app in link_contrib_apps if app in settings.INSTALLED_APPS]
    if link_apps_used:
        if "djangocms_link" not in settings.INSTALLED_APPS:
            errors.append(
                checks.Error(
                    "djangocms-frontend requires djangocms-link to be installed for {}.".format(
                        ", ".join(link_apps_used)
                    ),
                    "Add 'djangocms_link' to your INSTALLED_APPS setting or remove all of the above apps.",
                    id="djangocms_frontend.E001",
                    obj="settings.INSTALLED_APPS",
                )
            )
    return errors
