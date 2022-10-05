from importlib import import_module

from djangocms_frontend import settings

try:
    module = import_module(f"..{settings.framework}.background", __name__)
    BackgroundFormMixin = module.BackgroundFormMixin
    BackgroundMixin = module.BackgroundMixin
except ModuleNotFoundError:

    class BackgroundMixin:
        pass

    class BackgroundFormMixin:
        pass


def export(*args):
    """Dummy function to avoid linters to complain about unused imports"""
    return args


export(BackgroundMixin, BackgroundFormMixin)
