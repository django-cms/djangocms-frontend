from cms.plugin_pool import plugin_pool
from django.apps import apps
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template, insert_fields

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, SpacingMixin
from .. import link
from . import forms, models
from .constants import USE_LINK_ICONS
from .helpers import GetLinkMixin

mixin_factory = settings.get_renderer(link)


UILINK_FIELDS = (
    ("name", "link_type"),
    ("site", "url_grouper") if apps.is_installed("djangocms_url_manager") else "link",
    ("link_context", "link_size"),
    ("link_outline", "link_block"),
    "link_stretched",
)

UILINK_FIELDSET = [
    (
        None,
        {
            "fields": ("template",)
            + (UILINK_FIELDS + (("icon_left", "icon_right"),) if USE_LINK_ICONS else UILINK_FIELDS)
        },
    ),
]


class LinkPluginMixin:
    link_fieldset_position = None
    link_fields = (("site", "url_grouper"),) if apps.is_installed("djangocms_url_manager") else ("link", "target")

    def render(self, context, instance, placeholder):
        if "request" in context:
            instance._cms_page = getattr(context["request"], "current_page", None)
        context["mixin_link"] = instance.get_link()
        return super().render(context, instance, placeholder)

    def get_form(self, request, obj=None, change=False, **kwargs):
        """The link form needs the request object to check permissions"""
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        parent = obj.parent if obj else self._cms_initial_attributes.get("parent")
        form.name_required = parent and parent.plugin_type == "TextPlugin"
        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.link_fieldset_position is not None:
            fieldsets = insert_fields(
                fieldsets,
                self.link_fields,
                blockname=_("Link settings"),
                position=self.link_fieldset_position,
            )
        return fieldsets


class TextLinkPlugin(mixin_factory("Link"), AttributesMixin, SpacingMixin, LinkPluginMixin, GetLinkMixin, CMSUIPlugin):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    name = _("Link / Button")
    module = _("Frontend")
    model = models.Link
    form = forms.LinkForm
    change_form_template = "djangocms_frontend/admin/link.html"
    text_enabled = True
    text_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-link-45deg" '
        'viewBox="0 0 16 16"><path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 '
        "5.5L8 6.086a1 1 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4 4 0 0 "
        '1-.128-1.287z"/><path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 '
        '1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243z"/></svg>'
    )
    allow_children = True

    fieldsets = UILINK_FIELDSET

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "link", "link", settings.LINK_TEMPLATE_CHOICES)


if "djangocms_frontend.contrib.link" in django_settings.INSTALLED_APPS:
    #  Only register plugin if in INSTALLED_APPS
    plugin_pool.register_plugin(TextLinkPlugin)

    if "djangocms_link" in django_settings.INSTALLED_APPS:
        from djangocms_link.cms_plugins import LinkPlugin

        LinkPlugin.parent_classes = [""]  # Remove it from the list of valid plugins
