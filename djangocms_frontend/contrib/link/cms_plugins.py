from cms.plugin_pool import plugin_pool
from django.apps import apps
from django.conf import settings as django_settings
from django.urls import path
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template, insert_fields

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.spacing import SpacingMixin
from .. import link
from . import forms, models, views
from .constants import USE_LINK_ICONS

mixin_factory = settings.get_renderer(link)


UILINK_FIELDS = (
    ("name", "link_type"),
    ("site", "url_grouper") if apps.is_installed("djangocms_url_manager") else ("external_link", "internal_link"),
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
if not apps.is_installed("djangocms_url_manager"):
    UILINK_FIELDSET += [
        (
            _("Link settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("mailto", "phone"),
                    ("anchor", "target"),
                    ("file_link",),
                ),
            },
        ),
    ]


class LinkPluginMixin:
    link_fieldset_position = None
    link_fields = (
        (("site", "url_grouper"),)
        if apps.is_installed("djangocms_url_manager")
        else (
            ("external_link", "internal_link"),
            ("mailto", "phone"),
            ("anchor", "target"),
            "file_link",
        )
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        """The link form needs the request object to check permissions"""
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
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


class LinkPlugin(mixin_factory("Link"), AttributesMixin, SpacingMixin, LinkPluginMixin, CMSUIPlugin):
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

    def get_plugin_urls(self):
        return [
            path("autocomplete/", views.AutocompleteJsonView.as_view(), name="link_link_autocomplete"),
        ]


if "djangocms_frontend.contrib.link" in django_settings.INSTALLED_APPS and "LinkPlugin" not in plugin_pool.plugins:
    #  Only register plugin if in INSTALLED_APPS

    plugin_pool.register_plugin(LinkPlugin)
