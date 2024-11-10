from django import apps
from django.core import checks


class DjangocmsFrontendConfig(apps.AppConfig):
    name = "djangocms_frontend"
    verbose_name = "django CMS Frontend"

    def ready(self):
        from . import plugin_tag

        checks.register(check_settings)
        plugin_tag.setup()


def check_settings(*args, **kwargs):
    from django.conf import settings

    warnings = []

    if hasattr(settings, "DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH"):  # pragma: no cover
        warnings.append(checks.Warning(
            "The DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH setting was removed in djangocms-frontend 2.\n"
            "Use DJANGOCMS_LINK_MINIMUM_INPUT_LENGTH instead.",
            "This message disappears after removing the DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH from your project's "
            "settings.\n",
            id="djangocms_frontend.W001",
            obj="settings.DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH",
        ))
    if hasattr(settings, "DJANGOCMS_FRONTEND_LINK_MODELS"):  # pragma: no cover
        warnings.append(checks.Warning(
            "The DJANGOCMS_FRONTEND_LINK_MODELS setting was removed in djangocms-frontend 2.\n"
            "djangocms-frontend 2 uses linkable models from djangocms-link. See "
            "https://github.com/django-cms/djangocms-link#django-cms-link for more info.",
            "This message disappears after removing the DJANGOCMS_FRONTEND_LINK_MODELS from your project's settings.\n",
            id="djangocms_frontend.W002",
            obj="settings.DJANGOCMS_FRONTEND_LINK_MODELS",
        ))
    return warnings
