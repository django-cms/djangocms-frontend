from django import apps


class DjangocmsFrontendConfig(apps.AppConfig):
    name = "djangocms_frontend"
    verbose_name = "DjangoCMS Frontend"

    def ready(self):
        from .pool import setup

        setup()
