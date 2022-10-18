from importlib import import_module

from djangocms_frontend import settings

try:
    module = import_module(f"..{settings.framework}.sizing", __name__)
    SizingFormMixin = module.SizingFormMixin
    SizingMixin = module.SizingMixin
except ModuleNotFoundError:

    class SizingMixin:
        pass

    class SizingFormMixin:
        pass
