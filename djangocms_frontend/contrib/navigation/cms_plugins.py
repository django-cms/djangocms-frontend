from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.background import BackgroundMixin
from ...helpers import first_choice, get_plugin_template, get_template_path
from .. import navigation
from ..link.cms_plugins import LinkPlugin, LinkPluginMixin
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
    Creates a Navbar
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
        "NavContainerPlugin",
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
        return get_plugin_template(
            instance, "navigation", "navigation", settings.NAVIGATION_TEMPLATE_CHOICES
        )

    def render(self, context, instance, placeholder):
        context["nav_template"] = instance.config.get("template", default_template)
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class PageTreePlugin(
    mixin_factory("PageTree"),
    AttributesMixin,
    CMSUIPlugin,
):
    name = _("Page tree")
    module = _("Frontend")
    model = models.PageTree
    form = forms.PageTreeForm
    change_form_template = "djangocms_frontend/admin/page_tree.html"
    allow_children = False
    parent_classes = ["NavigationPlugin", "NavContainerPlugin"]
    fieldsets = [
        (
            None,
            {"fields": ("start_level",)},
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path(
            "navigation", context.get("nav_template", default_template), "page_tree"
        )

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
    name = _("Brand")
    module = _("Frontend")
    model = models.NavBrand
    form = forms.NavBrandForm
    change_form_template = "djangocms_frontend/admin/brand.html"
    allow_children = True
    parent_classes = ["NavigationPlugin", "NavContainerPlugin"]
    link_fieldset_position = -1

    fieldsets = [
        (
            None,
            {"fields": ("simple_content",)},
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path(
            "navigation", context.get("nav_template", default_template), "brand"
        )


@plugin_pool.register_plugin
class NavContainerPlugin(
    mixin_factory("NavLink"),
    AttributesMixin,
    CMSUIPlugin,
):
    name = _("Navigation container")
    module = _("Frontend")
    model = models.NavContainer
    form = forms.NavContainerForm
    change_form_template = "djangocms_frontend/admin/nav_container.html"
    allow_children = True
    parent_classes = ["NavigationPlugin"]
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

    def get_render_template(self, context, instance, placeholder):
        return get_template_path(
            "navigation", context.get("nav_template", default_template), "nav_container"
        )


@plugin_pool.register_plugin
class NavLinkPlugin(
    mixin_factory("NavLink"),
    LinkPlugin,
):
    name = _("Navigation link")
    module = _("Frontend")
    model = models.NavLink
    form = forms.NavLinkForm
    change_form_template = "djangocms_frontend/admin/navlink.html"
    allow_children = True
    parent_classes = ["NavigationPlugin", "NavContainerPlugin", "NavLinkPlugin"]
    child_classes = [
        "NavLinkPlugin",
        "GridContainerPlugin",
        "GridRowPlugin",
        "ListGroupPlugin",
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_template_path(
            "navigation", context.get("nav_template", default_template), "link"
        )
