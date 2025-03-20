from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, BackgroundMixin, ResponsiveMixin, SpacingMixin
from .. import content
from . import forms, models

mixin_factory = settings.get_renderer(content)


@plugin_pool.register_plugin
class CodePlugin(
    mixin_factory("Code"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    name = _("Code")
    module = _("Frontend")
    model = models.CodeBlock
    form = forms.CodeForm
    change_form_template = "djangocms_frontend/admin/code.html"

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "code_content",
                    "code_type",
                )
            },
        ),
    ]


@plugin_pool.register_plugin
class BlockquotePlugin(
    mixin_factory("Blockquote"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    name = _("Blockquote")
    module = _("Frontend")
    model = models.Blockquote
    form = forms.BlockquoteForm
    change_form_template = "djangocms_frontend/admin/blockquote.html"
    allow_children = True
    frontend_editable_fields = ("quote_content", "quote_origin")

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "quote_content",
                    "quote_origin",
                    "quote_alignment",
                )
            },
        ),
    ]


@plugin_pool.register_plugin
class FigurePlugin(
    mixin_factory("Figure"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    name = _("Figure")
    module = _("Frontend")
    model = models.Figure
    form = forms.FigureForm
    change_form_template = "djangocms_frontend/admin/figure.html"
    allow_children = True
    frontend_editable_fields = ("figure_caption",)

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "figure_caption",
                    "figure_alignment",
                )
            },
        ),
    ]
