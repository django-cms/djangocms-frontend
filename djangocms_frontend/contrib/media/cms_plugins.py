from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from .. import media
from . import forms, models

mixin_factory = settings.get_renderer(media)


@plugin_pool.register_plugin
class MediaPlugin(mixin_factory("Media"), CMSUIPlugin):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    name = _("Media")
    module = _("Frontend")
    model = models.Media
    form = forms.MediaForm
    change_form_template = "djangocms_frontend/admin/media.html"
    allow_children = True

    fieldsets = [
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


@plugin_pool.register_plugin
class MediaBodyPlugin(mixin_factory("MediaBody"), CMSUIPlugin):
    """
    Layout > "Media body" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    name = _("Media body")
    module = _("Frontend")
    model = models.MediaBody
    form = forms.MediaBodyForm
    change_form_template = "djangocms_frontend/admin/media.html"
    allow_children = True
    parent_classes = ["MediaPlugin"]

    fieldsets = [
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
