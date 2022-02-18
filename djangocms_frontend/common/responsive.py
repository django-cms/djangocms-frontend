from djangocms_frontend import settings

if settings.framework == "bootstrap5":
    from .bootstrap5.responsive import ResponsiveFormMixin, ResponsiveMixin
else:

    class ResponsiveMixin:
        pass

    class ResponsiveFormMixin:
        pass
