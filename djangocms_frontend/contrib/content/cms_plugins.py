from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class CodePlugin(CMSPluginBase):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    name = _("Code")
    module = _("Interface")
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
class BlockquotePlugin(CMSPluginBase):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    name = _("Blockquote")
    module = _("Interface")
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

    def render(self, context, instance, placeholder):
        link_classes = ["blockquote"]
        if instance.quote_alignment:
            link_classes.append(instance.quote_alignment)
        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class FigurePlugin(CMSPluginBase):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    name = _("Figure")
    module = _("Interface")
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

    def render(self, context, instance, placeholder):
        classes = concat_classes(
            [
                "figure",
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
