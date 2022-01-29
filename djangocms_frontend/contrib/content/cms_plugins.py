from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import content
from . import forms, models

mixin_factory = settings.get_renderer(content)


@plugin_pool.register_plugin
class CodePlugin(mixin_factory("Code"), CMSPluginBase):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    name = _("Code")
    module = _("Frontend")
    model = models.CodeBlock
    form = forms.CodeForm
    render_template = f"djangocms_frontend/{settings.framework}/code.html"
    change_form_template = "djangocms_frontend/admin/code.html"
    text_enabled = True

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
        (_("Advanced settings"), {"classes": ("collapse",), "fields": ("attributes",)}),
    ]


@plugin_pool.register_plugin
class BlockquotePlugin(mixin_factory("Blockquote"), CMSPluginBase):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    name = _("Blockquote")
    module = _("Frontend")
    model = models.Blockquote
    form = forms.BlockquoteForm
    render_template = f"djangocms_frontend/{settings.framework}/blockquote.html"
    change_form_template = "djangocms_frontend/admin/blockquote.html"
    text_enabled = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("quote_content", "quote_origin"),
                    "quote_alignment",
                )
            },
        ),
        (_("Advanced settings"), {"classes": ("collapse",), "fields": ("attributes",)}),
    ]


@plugin_pool.register_plugin
class FigurePlugin(mixin_factory("Figure"), CMSPluginBase):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    name = _("Figure")
    module = _("Frontend")
    model = models.Figure
    form = forms.FigureForm
    render_template = f"djangocms_frontend/{settings.framework}/figure.html"
    change_form_template = "djangocms_frontend/admin/figure.html"
    allow_children = True

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
        (_("Advanced settings"), {"classes": ("collapse",), "fields": ("attributes",)}),
    ]
