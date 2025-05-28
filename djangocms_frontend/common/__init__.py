from importlib import import_module

from djangocms_frontend import settings

from .attributes import AttributesFormMixin, AttributesMixin
from .title import TitleFormMixin, TitleMixin

__common = {
    "background": ("BackgroundFormMixin", "BackgroundMixin"),
    "responsive": ("ResponsiveFormMixin", "ResponsiveMixin"),
    "sizing": ("SizingFormMixin", "SizingMixin"),
    "spacing": (
        "SpacingFormMixin",
        "SpacingMixin",
        "MarginFormMixin",
        "MarginMixin",
        "PaddingFormMixin",
        "PaddingMixin",
    ),
}

for module, classes in __common.items():
    try:
        module = import_module(f"{__name__}.{settings.framework}.{module}", module)
        for cls in classes:
            globals()[cls] = getattr(module, cls)
    except ModuleNotFoundError:  # pragma: no cover
        for cls in classes:
            globals()[cls] = type(cls, (object,), {})

__all__ = [
    "TitleMixin",
    "TitleFormMixin",
    "AttributesMixin",
    "AttributesFormMixin",
    "BackgroundFormMixin",
    "BackgroundMixin",
    "ResponsiveFormMixin",
    "ResponsiveMixin",
    "SizingFormMixin",
    "SizingMixin",
    "SpacingFormMixin",
    "SpacingMixin",
    "MarginFormMixin",
    "MarginMixin",
    "PaddingFormMixin",
    "PaddingMixin",
]
