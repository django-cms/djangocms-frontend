from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, BackgroundMixin, MarginMixin, PaddingMixin, ResponsiveMixin
from ...helpers import add_plugin
from .. import card
from . import forms, models

mixin_factory = settings.get_renderer(card)


@plugin_pool.register_plugin
class CardLayoutPlugin(mixin_factory("CardLayout"), AttributesMixin, CMSUIPlugin):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card layout")
    module = _("Frontend")
    model = models.CardLayout
    form = forms.CardLayoutForm
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
                "fields": ([f"row_cols_{size}" for size in settings.DEVICE_SIZES],),
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for pos in range(data["create"] if data["create"] is not None else 0):
            add_plugin(
                obj.placeholder,
                models.Card(
                    parent=obj,
                    placeholder=obj.placeholder,
                    position=obj.position + 1 + pos,
                    language=obj.language,
                    plugin_type=CardPlugin.__name__,
                    ui_item=models.Card.__class__.__name__,
                ).initialize_from_form(forms.CardForm),
            )


@plugin_pool.register_plugin
class CardPlugin(
    mixin_factory("Card"),
    AttributesMixin,
    ResponsiveMixin,
    MarginMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card")
    module = _("Frontend")
    model = models.Card
    form = forms.CardForm
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
                    (
                        "card_text_color",
                        "card_outline",
                    ),
                    "card_full_height",
                )
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            add_plugin(
                obj.placeholder,
                models.CardInner(
                    parent=obj,
                    position=obj.position + 1,
                    placeholder=obj.placeholder,
                    language=obj.language,
                    plugin_type=CardInnerPlugin.__name__,
                    ui_item=models.CardInner.__class__.__name__,
                    config=dict(inner_type="card-body"),
                ),
            )


@plugin_pool.register_plugin
class CardInnerPlugin(
    mixin_factory("CardInner"),
    AttributesMixin,
    ResponsiveMixin,
    PaddingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Card inner")
    module = _("Frontend")
    model = models.CardInner
    form = forms.CardInnerForm
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
                    "text_alignment",
                )
            },
        ),
    ]
