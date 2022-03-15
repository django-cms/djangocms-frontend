from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.background import BackgroundMixin
from ...helpers import get_plugin_template
from .. import navigation
from . import forms, models

mixin_factory = settings.get_renderer(navigation)


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
    child_classes = ["LinkPlugin", "PageTreePlugin", "BrandPlugin"]

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


@plugin_pool.register_plugin
class PageTreePlugin(
    mixin_factory("PageTree"),
    AttributesMixin,
    CMSUIPlugin,
):
    """
    Creates a Navbar
    """

    name = _("Page tree")
    module = _("Frontend")
    model = models.PageTree
    form = forms.PageTreeForm
    change_form_template = "djangocms_frontend/admin/page_tree.html"
    allow_children = False
    parent_classes = ["NavigationPlugin"]
    fieldsets = [
        (
            None,
            {"fields": ("template",)},
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "navigation", "page_tree", settings.NAVIGATION_TEMPLATE_CHOICES
        )


@plugin_pool.register_plugin
class BrandPlugin(
    mixin_factory("Brand"),
    AttributesMixin,
    CMSUIPlugin,
):
    """
    Creates a Navbar
    """

    name = _("Brand")
    module = _("Frontend")
    model = models.Brand
    form = forms.BrandForm
    change_form_template = "djangocms_frontend/admin/brand.html"
    allow_children = True
    parent_classes = ["NavigationPlugin"]

    fieldsets = [
        (
            None,
            {"fields": ("simple_content",)},
        ),
    ]
