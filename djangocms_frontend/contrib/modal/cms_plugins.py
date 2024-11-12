from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from .. import modal
from . import forms, models

mixin_factory = settings.get_renderer(modal)


@plugin_pool.register_plugin
class ModalPlugin(mixin_factory("Modal"), AttributesMixin, CMSUIPlugin):
    """
    Component > "Modal" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    name = _("Modal")
    module = _("Frontend")
    model = models.Modal
    form = forms.ModalForm
    change_form_template = "djangocms_frontend/admin/modal.html"
    allow_children = True
    child_classes = [
        "ModalTriggerPlugin",
        "ModalContainerPlugin",
    ]

    fieldsets = [
        (None, {"fields": ("modal_siblings",)}),
    ]


@plugin_pool.register_plugin
class ModalTriggerPlugin(mixin_factory("ModalTrigger"), AttributesMixin, CMSUIPlugin):
    """
    Component > "Modal" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    name = _("Modal trigger")
    module = _("Frontend")
    model = models.ModalTrigger
    form = forms.ModalTriggerForm
    allow_children = True
    parent_classes = [
        "ModalPlugin"
    ]

    fieldsets = [
        (None, {"fields": ("trigger_identifier",)}),
    ]


@plugin_pool.register_plugin
class ModalContainerPlugin(mixin_factory("ModalContainer"), CMSUIPlugin):
    """
    Component > "Modal Container" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    name = _("Modal container")
    module = _("Frontend")
    model = models.ModalContainer
    form = forms.ModalContainerForm
    allow_children = True
    parent_classes = [
        "ModalPlugin"
    ]
    child_classes = [
        "ModalInnerPlugin",

    ]
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "container_identifier",
                    ("modal_centered"),
                    ("modal_static", "modal_scrollable"),
                    ("modal_size", "modal_fullscreen"),
                )
            }
        ),
    ]


@plugin_pool.register_plugin
class ModalInnerPlugin(
    mixin_factory("ModalInner"),
    CMSUIPlugin,
):
    """
    Component > "Modal Container Content" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """
    name = _("Modal inner")
    module = _("Frontend")
    model = models.ModalInner
    form = forms.ModalInnerForm
    allow_children = True
    parent_classes = [
        "ModalContainerPlugin",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "inner_type",
                    "attributes",
                )
            },
        ),
    ]
