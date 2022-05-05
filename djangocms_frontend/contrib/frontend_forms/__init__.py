import hashlib

from django.utils.translation import gettext_lazy as _

_form_registry = {}


def verbose_name(form_class):
    """returns the verbose_name property of a Meta class if present or else
    splits the camel-cased form class name"""
    if hasattr(form_class, "Meta") and hasattr(form_class.Meta, "verbose_name"):
        return getattr(form_class.Meta, "verbose_name")  # noqa
    class_name = form_class.__name__.rsplit(".", 1)[-1]
    from re import finditer

    matches = finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", class_name
    )
    return " ".join(m.group(0) for m in matches)


def get_registered_forms():
    """Creates a tuple for a ChoiceField to select form"""
    result = tuple(
        (hash, verbose_name(form_class)) for hash, form_class in _form_registry.items()
    )
    return result if result else ((_("No forms registered"), ()),)


def register_with_frontend(form_class):
    """Function to call or decorator for a Form class to make it available for the
    djangocms_frontend.contrib.frontend_forms plugin"""
    hash = hashlib.sha1(form_class.__name__.encode("utf-8")).hexdigest()
    _form_registry.update({hash: form_class})
    return form_class


__all__ = ["register_with_frontend", "get_registered_forms"]
