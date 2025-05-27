import importlib

from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _

EMPTY_CHOICE = (("", "-----"),)

EMPTY_FIELDSET = [
    (
        None,
        {
            "fields": (),
            "description": _("There are no further settings for this plugin. Please press save."),
        },
    )
]

# Only adding block elements
TAG_CHOICES = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_TAG_CHOICES",
    ["div", "section", "article", "header", "footer", "aside"],
)
TAG_CHOICES = tuple((entry, entry) for entry in TAG_CHOICES)

ADMIN_CSS = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_ADMIN_CSS",
    {},
)

HEADER_CHOICES = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_HEADER_CHOICES",
    (
        ("h1", _("Heading 1")),
        ("h2", _("Heading 2")),
        ("h3", _("Heading 3")),
        ("h4", _("Heading 4")),
        ("h5", _("Heading 5")),
    ),
)

ALIGN_CHOICES = (
    ("start", _("Left")),
    ("center", _("Center")),
    ("end", _("Right")),
)

LINK_TEMPLATE_CHOICES = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_LINK_TEMPLATE_CHOICES",
    [
        ("default", _("Default")),
    ],
)

JUMBOTRON_TEMPLATE_CHOICES = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_JUMBOTRON_TEMPLATE_CHOICES",
    [
        ("default", _("Default")),
    ],
)

NAVIGATION_TEMPLATE_CHOICES = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_NAVIGATION_TEMPLATE_CHOICES",
    [
        ("default", _("Default")),
        ("offcanvas", _("Offcanvas")),
    ],
)

SHOW_EMPTY_CHILDREN = getattr(django_settings, "DJANGOCMS_FRONTEND_SHOW_EMPTY_CHILDREN", False)

FORM_OPTIONS = getattr(django_settings, "DJANGOCMS_FRONTEND_FORM_OPTIONS", {})

COMPONENT_FIELDS = getattr(django_settings, "DJANGOCMS_FRONTEND_COMPONENT_FIELDS", {})
COMPONENT_FOLDER = getattr(django_settings, "DJANGOCMS_FRONTEND_COMPONENT_FOLDER", "cms_components")
framework = getattr(django_settings, "DJANGOCMS_FRONTEND_FRAMEWORK", "bootstrap5")
theme = getattr(django_settings, "DJANGOCMS_FRONTEND_THEME", "djangocms_frontend")

framework_settings = importlib.import_module(f"djangocms_frontend.frameworks.{framework}")

DEVICE_SIZES = framework_settings.DEVICE_SIZES
DEVICE_CHOICES = framework_settings.DEVICE_CHOICES
COLOR_STYLE_CHOICES = framework_settings.COLOR_STYLE_CHOICES
# COLOR_CODES = framework_settings.COLOR_CODES
FORM_TEMPLATE = getattr(framework_settings, "FORM_TEMPLATE", None)
SPACER_PROPERTY_CHOICES = framework_settings.SPACER_PROPERTY_CHOICES
SPACER_SIDE_CHOICES = framework_settings.SPACER_SIDE_CHOICES
SPACER_SIZE_CHOICES = framework_settings.SPACER_SIZE_CHOICES
SPACER_X_SIDES_CHOICES = framework_settings.SPACER_X_SIDES_CHOICES
SPACER_Y_SIDES_CHOICES = framework_settings.SPACER_Y_SIDES_CHOICES
SIZE_X_CHOICES = framework_settings.SIZE_X_CHOICES
SIZE_Y_CHOICES = framework_settings.SIZE_Y_CHOICES
NAVBAR_DESIGNS = framework_settings.NAVBAR_DESIGNS

FRAMEWORK_PLUGIN_INFO = getattr(framework_settings, "FRAMEWORK_PLUGIN_INFO", dict())

EXCL_COL_PROP = FRAMEWORK_PLUGIN_INFO.get("GridColumn", {}).get("excl_col_prop", [])
EXCL_CARD_PROP = FRAMEWORK_PLUGIN_INFO.get("Card", {}).get("excl_card_prop", [])

theme_render_path = f"{theme}.frameworks.{framework}"
theme_forms_path = f"{theme}.forms"


def render_factory(cls, theme_module, render_module):
    parents = tuple(
        getattr(module, cls, None)
        for module in (theme_module, render_module)
        if module is not None and getattr(module, cls, None) is not None
    )
    return type(cls, parents, dict())  # Empty Mix


def get_mixins(naming, theme_path, mixin_path):
    try:
        theme_module = importlib.import_module(theme_path) if theme_path else None
    except ModuleNotFoundError:
        theme_module = None
    try:
        render_module = importlib.import_module(mixin_path) if mixin_path else None
    except ModuleNotFoundError:
        render_module = None

    return lambda name: render_factory(naming.format(name=name), theme_module, render_module)


def get_renderer(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins("{name}RenderMixin", theme_render_path, f"{my_module}.frameworks.{framework}")


def get_forms(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins("{name}FormMixin", theme_forms_path, f"{my_module}.frameworks.{framework}")
