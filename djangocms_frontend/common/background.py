from djangocms_frontend import settings

if settings.framework == "bootstrap5":
    from .bootstrap5.background import BackgroundFormMixin, BackgroundMixin
else:

    class BackgroundMixin:
        pass

    class BackgroundFormMixin:
        pass
