from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, BackgroundMixin
from ...helpers import first_choice, get_plugin_template, get_template_path
from .. import navigation
from ..link.cms_plugins import LinkPluginMixin, TextLinkPlugin
from . import forms, models

mixin_factory = settings.get_renderer(navigation)

default_template = first_choice(settings.NAVIGATION_TEMPLATE_CHOICES)


@plugin_pool.register_plugin
class NavigationPlugin(
    mixin_factory("Navigation"),
    AttributesMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    The NavigationPlugin class is a plugin used in Django CMS to create navigation menus or off-canvas menus.
    """

    name = _("Navigation")
    module = _("Frontend")
    model = models.Navigation
    form = forms.NavigationForm
    change_form_template = "djangocms_frontend/admin/navigation.html"
    allow_children = True
    child_classes = [
        "NavLinkPlugin",
        "PageTreePlugin",
        "NavBrandPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    (
                        "navbar_design",
                        "navbar_breakpoint",
                    ),
                    "navbar_container",
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "navigation", "navigation", settings.NAVIGATION_TEMPLATE_CHOICES)

    def render(self, context, instance, placeholder):
        context["nav_template"] = instance.config.get("template", default_template)
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class PageTreePlugin(
    mixin_factory("PageTree"),
    AttributesMixin,
    CMSUIPlugin,
):
    """

    The PageTreePlugin class is a plugin for Django CMS that allows users to display a hierarchical
    tree-like structure of pages on the frontend.
    """

    name = _("Page tree")
    module = _("Frontend")
    model = models.PageTree
    form = forms.PageTreeForm
    change_form_template = "djangocms_frontend/admin/page_tree.html"
    allow_children = False
    parent_classes = [
        "NavigationPlugin",
    ]
    show_add_form = False
    fieldsets = [
        (
            None,
            {"fields": ("start_level",)},
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path("navigation", context.get("nav_template", default_template), "page_tree")

    def render(self, context, instance, placeholder):
        context["start_level"] = instance.config.get("start_level", 0)
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class NavBrandPlugin(
    mixin_factory("NavBrand"),
    AttributesMixin,
    LinkPluginMixin,
    CMSUIPlugin,
):
    """
    The `NavBrandPlugin` class is a plugin used in Django CMS to create a navigation brand element.
    This plugin allows the user to define a brand logo or text that will be displayed in the
    navigation header. Content is added through child plugins.
    """

    name = _("Brand")
    module = _("Frontend")
    model = models.NavBrand
    form = forms.NavBrandForm
    change_form_template = "djangocms_frontend/admin/brand.html"
    allow_children = True
    parent_classes = [
        "NavigationPlugin",
    ]
    link_fieldset_position = -1

    fieldsets = [
        (
            None,
            {"fields": ("simple_content",)},
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path("navigation", context.get("nav_template", default_template), "brand")


@plugin_pool.register_plugin
class NavContainerPlugin(
    mixin_factory("NavLink"),
    AttributesMixin,
    CMSUIPlugin,
):
    """
    The `NavContainerPlugin` class is a deprecated plugin without functionality. It will be removed.
    """

    name = _("Navigation container")
    module = _("Frontend")
    model = models.NavContainer
    change_form_template = "djangocms_frontend/admin/deprecated.html"
    allow_children = True
    parent_classes = [""]  # No parent classes
    child_classes = [
        "NavLinkPlugin",
        "PageTreePlugin",
        "NavBrandPlugin",
    ]

    fieldsets = [
        (
            None,
            {"fields": ()},
        ),
    ]


@plugin_pool.register_plugin
class NavLinkPlugin(
    mixin_factory("NavLink"),
    TextLinkPlugin,
):
    """
    A plugin that allows creating navigation links for the frontend.

    Attributes:
    -----------
    - `name` (str): The name of the plugin, displayed in the plugin list when editing a page.
    - `module` (str): The module where the plugin belongs, displayed in the plugin list when editing a page.
    - `model` (Model): The Django model used to store the plugin's data.
    - `form` (Form): The form used to render the plugin's settings in the admin interface.
    - `change_form_template` (str): The path to the template used to render the plugin's change form in the admin
      interface.
    - `allow_children` (bool): Whether the plugin allows having child plugins.
    - `parent_classes` (list): List of parent plugin classes that this plugin can be nested within.
    - `child_classes` (list): List of child plugin classes that can be nested within this plugin.
    """

    name = _("Navigation link")
    module = _("Frontend")
    model = models.NavLink
    form = forms.NavLinkForm
    change_form_template = "djangocms_frontend/admin/navlink.html"
    allow_children = True
    parent_classes = ["NavigationPlugin", "NavLinkPlugin"]
    child_classes = [
        "NavLinkPlugin",
        "GridContainerPlugin",
        "GridRowPlugin",
        "ListGroupPlugin",
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path("navigation", context.get("nav_template", default_template), "link")
