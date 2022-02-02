from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from .. import card
from . import forms, models

mixin_factory = settings.get_renderer(card)


@plugin_pool.register_plugin
class CardLayoutPlugin(mixin_factory("CardLayout"), CMSPluginBase):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card layout")
    module = _("Frontend")
    model = models.CardLayout
    form = forms.CardLayoutForm
    render_template = f"djangocms_frontend/{settings.framework}/card_layout.html"
    change_form_template = "djangocms_frontend/admin/card_layout.html"
    allow_children = True
    child_classes = [
        "CardPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "card_type",
                        "create",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": (
                    ["row_cols_{}".format(size) for size in settings.DEVICE_SIZES],
                ),
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for x in range(data["create"] if data["create"] is not None else 0):
            col = models.Card(
                parent=obj,
                placeholder=obj.placeholder,
                language=obj.language,
                position=obj.numchild,
                plugin_type=CardPlugin.__name__,
                ui_item=models.Card.__class__.__name__,
            ).initialize_from_form(forms.CardForm)
            obj.add_child(instance=col)


@plugin_pool.register_plugin
class CardPlugin(mixin_factory("Card"), CMSPluginBase):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card")
    module = _("Frontend")
    model = models.Card
    form = forms.CardForm
    render_template = f"djangocms_frontend/{settings.framework}/card.html"
    change_form_template = "djangocms_frontend/admin/card.html"
    allow_children = True
    child_classes = [
        "CardInnerPlugin",
        "ListGroupPlugin",
        "ImagePlugin",
        "GridRowPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "card_alignment",
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

    def save_model(self, request, obj, form, change):
        new_card = obj.id is None
        super().save_model(request, obj, form, change)
        if new_card:
            obj.add_child(
                instance=models.CardInner(
                    parent=obj,
                    placeholder=obj.placeholder,
                    position=obj.numchild,
                    language=obj.language,
                    plugin_type=CardInnerPlugin.__name__,
                    ui_item=models.CardInner.__class__.__name__,
                    config=dict(inner_type="card-body"),
                )
            )


@plugin_pool.register_plugin
class CardInnerPlugin(mixin_factory("CardInner"), CMSPluginBase):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card inner")
    module = _("Frontend")
    model = models.CardInner
    form = forms.CardInnerForm
    render_template = f"djangocms_frontend/{settings.framework}/card_content.html"
    change_form_template = "djangocms_frontend/admin/card.html"
    allow_children = True
    parent_classes = [
        "CardPlugin",
        "CollapseTriggerPlugin",
        "CollapseContainerPlugin",
        "GridColumnPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "inner_type",
                    (
                        "inner_context",
                        "text_alignment",
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
