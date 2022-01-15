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
                    (
                        "card_type",
                        "card_alignment",
                    ),
                    ("card_context", "card_text_color"),
                    (
                        "card_outline",
                        "card_full_height",
                    ),
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
        if getattr(instance, "card_full_height", False):
            link_classes.append("h-100")
        context["add_classes"] = " ".join(link_classes)
        return super().render(context, instance, placeholder)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if self.card_type == "card":
    #         obj.add_child(
    #             instance=models.CardInner(
    #                 parent=obj,
    #                 placeholder=obj.placeholder,
    #                 position=obj.numchild,
    #                 language=obj.language,
    #                 plugin_type=CardInnerPlugin.__name__,
    #                 ui_item=models.CardInner.__class__.__name__,
    #                 config=dict(inner_type="card-body"),
    #             )
    #         )


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
    render_template = f"djangocms_frontend/{settings.framework}/card_content.html"
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
