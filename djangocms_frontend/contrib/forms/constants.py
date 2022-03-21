import importlib

from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings

framework = importlib.import_module(
    f"djangocms_frontend.contrib.forms.frontends.{settings.framework}",
)

default_attr = framework.default_attr  # NOQA
attr_dict = framework.attr_dict  # NOQA
DEFAULT_FIELD_SEP = framework.DEFAULT_FIELD_SEP  # NOQA

CHOICE_FIELDS = (
    ("select", _("Drop down (single choice)")),
    ("multiselect", _("List (multiple choice)")),
    ("radio", _("Radio buttons (single choice)")),
    ("checkbox", _("Checkboxes (multiple choice)")),
)
