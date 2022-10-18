from importlib import import_module

from djangocms_frontend import settings

try:
    module = import_module(f"..{settings.framework}.responsive", __name__)
    ResponsiveFormMixin = module.ResponsiveFormMixin
    ResponsiveMixin = module.ResponsiveMixin
except ModuleNotFoundError:

    class ResponsiveMixin:
        pass

    class ResponsiveFormMixin:
        pass
