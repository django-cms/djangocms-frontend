from djangocms_frontend import settings

if settings.framework == "bootstrap5":
    from .bootstrap5.sizing import SizingFormMixin, SizingMixin
else:

    class SizingMixin:
        pass

    class SizingFormMixin:
        pass
