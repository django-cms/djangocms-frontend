from importlib import import_module

from djangocms_frontend import settings
from djangocms_frontend.helpers import export

try:
    module = import_module(f"..{settings.framework}.responsive", __name__)
    ResponsiveFormMixin = module.ResponsiveFormMixin
    ResponsiveMixin = module.ResponsiveMixin
except ModuleNotFoundError:

    class ResponsiveMixin:
        pass

    class ResponsiveFormMixin:
        pass


export(ResponsiveFormMixin, ResponsiveMixin)
