from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from djangocms_link.cms_plugins import LinkPlugin
from djangocms_link.models import get_templates

from djangocms_frontend.helpers import concat_classes, get_plugin_template

from . import forms, models
from .constants import USE_LINK_ICONS


class UILinkPlugin(LinkPlugin):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    name = _("Link / Button")
    module = _("Interface")
    model = models.Link
    form = forms.LinkForm
    change_form_template = "djangocms_frontend/admin/link.html"

    fields = (
        ("name", "link_type"),
        ("external_link", "internal_link"),
        ("link_context", "link_size"),
        ("link_outline", "link_block"),
    )

    if USE_LINK_ICONS:  # pragma: no cover
        fields = fields + (("icon_left", "icon_right"),)

    LinkPlugin.fieldsets[0] = (None, {"fields": fields})

    fieldsets = LinkPlugin.fieldsets

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "link", "link", get_templates())

    def render(self, context, instance, placeholder):
        link_classes = []
        if instance.link_context:
            if instance.link_type == "link":
                link_classes.append("text-{}".format(instance.link_context))
            else:
                link_classes.append("btn")
                if not instance.link_outline:
                    link_classes.append("btn-{}".format(instance.link_context))
                else:
                    link_classes.append("btn-outline-{}".format(instance.link_context))
        if instance.link_size:
            link_classes.append(instance.link_size)
        if instance.link_block:
            link_classes.append("btn-block")

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)


# plugin_pool.unregister_plugin(LinkPlugin)
plugin_pool.register_plugin(UILinkPlugin)
