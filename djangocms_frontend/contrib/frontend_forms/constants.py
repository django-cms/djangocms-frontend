import importlib

from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings

framework = importlib.import_module(
    f"djangocms_frontend.contrib.frontend_forms.frontends.{settings.framework}",
)

default_attr = framework.default_attr  # NOQA
attr_dict = framework.attr_dict  # NOQA
DEFAULT_FIELD_SEP = framework.DEFAULT_FIELD_SEP  # NOQA

CHOICE_FIELDS = (
    (
        _("Single choice"),
        (
            ("select", _("Drop down")),
            ("radio", _("Radio buttons")),
        ),
    ),
    (
        _("Multiple choice"),
        (
            ("checkbox", _("Checkboxes")),
            ("multiselect", _("List")),
        ),
    ),
)
