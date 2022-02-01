import importlib

from djangocms_frontend import settings

framework = importlib.import_module(
    f"djangocms_frontend.contrib.forms.frontends.{settings.framework}",
)

default_attr = framework.default_attr  # NOQA
attr_dict = framework.attr_dict  # NOQA
DEFAULT_FIELD_SEP = framework.DEFAULT_FIELD_SEP  # NOQA
