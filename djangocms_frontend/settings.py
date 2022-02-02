import importlib

from django.conf import settings
from django.utils.translation import gettext_lazy as _

EMPTY_CHOICE = (("", "------"),)

# Only adding block elements
TAG_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_TAG_CHOICES",
    ["div", "section", "article", "header", "footer", "aside"],
)
TAG_CHOICES = tuple((entry, entry) for entry in TAG_CHOICES)

ADMIN_CSS = getattr(
    settings,
    "DJANGOCMS_FRONTEND_ADMIN_CSS",
    {},
)

HEADER_CHOICES = getattr(
    settings,
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
    settings,
    "DJANGOCMS_FRONTEND_LINK_TEMPLATE_CHOICES",
    [
        ("default", _("Default")),
    ],
)


IMAGE_POSITIONING = (
    ("center center", _("Fully Centered")),
    ("left top", _("Top left")),
    ("center top", _("Top center")),
    ("right top", _("Top right")),
    ("left center", _("Center left")),
    ("right center", _("Center right")),
    ("left bottom", _("Bottom left")),
    ("center bottom", _("Bottom center")),
    ("right bottom", _("Bottom right")),
)

framework = getattr(settings, "DJANGOCMS_FRONTEND_FRAMEWORK", "bootstrap5")
theme = getattr(settings, "DJANGOCMS_FRONTEND_THEME", "djangocms_frontend")

framework_settings = importlib.import_module(
    f"djangocms_frontend.frontends.{framework}"
)

DEVICE_SIZES = framework_settings.DEVICE_SIZES
DEVICE_CHOICES = framework_settings.DEVICE_CHOICES
COLOR_STYLE_CHOICES = framework_settings.COLOR_STYLE_CHOICES
COLOR_CODES = framework_settings.COLOR_CODES
FORM_TEMPLATE = framework_settings.FORM_TEMPLATE
SPACER_PROPERTY_CHOICES = framework_settings.SPACER_PROPERTY_CHOICES
SPACER_SIDE_CHOICES = framework_settings.SPACER_SIDE_CHOICES
SPACER_SIZE_CHOICES = framework_settings.SPACER_SIZE_CHOICES
FRAMEWORK_PLUGIN_INFO = getattr(framework_settings, "FRAMEWORK_PLUGIN_INFO", dict())

theme_render_path = f"{theme}.frameworks.{framework}"
theme_forms_path = f"{theme}.forms"


def render_factory(cls, theme_module, render_module):
    parents = tuple(
        getattr(module, cls, None)
        for module in (render_module, theme_module)
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

    return lambda name: render_factory(
        naming.format(name=name), theme_module, render_module
    )


def get_renderer(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins(
        "{name}RenderMixin", theme_render_path, f"{my_module}.frameworks.{framework}"
    )


def get_forms(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins(
        "{name}FormMixin", theme_forms_path, f"{my_module}.frameworks.{framework}"
    )
