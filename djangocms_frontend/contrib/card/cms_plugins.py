from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class CardPlugin(CMSPluginBase):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card")
    module = _("Interface")
    model = models.Card
    form = forms.CardForm
    render_template = f"djangocms_frontend/{settings.framework}/card.html"
    change_form_template = "djangocms_frontend/admin/card.html"
    allow_children = True
    child_classes = [
        "CardPlugin",
        "CardInnerPlugin",
        "LinkPlugin",
        "ListGroupPlugin",
        "PicturePlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "card_type",
                    ("card_context", "card_text_color"),
                    ("card_alignment", "card_outline"),
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        link_classes = [instance.card_type]
        if instance.card_context and instance.card_outline:
            link_classes.append("border-{}".format(instance.card_context))
        elif instance.card_context:
            link_classes.append("bg-{}".format(instance.card_context))
        if instance.card_alignment:
            link_classes.append(instance.card_alignment)
        if instance.card_text_color:
            link_classes.append("text-{}".format(instance.card_text_color))

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CardInnerPlugin(CMSPluginBase):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card inner")
    module = _("Interface")
    model = models.CardInner
    form = forms.CardInnerForm
    render_template = f"djangocms_frontend/{settings.framework}/card.html"
    change_form_template = "djangocms_frontend/admin/card.html"
    allow_children = True
    parent_classes = [
        "CardPlugin",
        "CollapseTriggerPlugin",
        "CollapseContainerPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("inner_type",)}),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        classes = concat_classes(
            [instance.inner_type]
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
