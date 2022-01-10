from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend.helpers import concat_classes

from ... import settings
from ...models import FrontendUIItem
from . import models


class EmptyForm(EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {"config": []}
        untangled_fields = ("tag_type", "attributes")


@plugin_pool.register_plugin
class MediaPlugin(CMSPluginBase):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    name = _("Media")
    module = _("Frontend")
    model = models.Media
    form = EmptyForm
    render_template = f"djangocms_frontend/{settings.framework}/media.html"
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
class MediaBodyPlugin(CMSPluginBase):
    """
    Layout > "Media body" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    name = _("Media body")
    module = _("Frontend")
    model = models.MediaBody
    form = EmptyForm
    render_template = f"djangocms_frontend/{settings.framework}/media-body.html"
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
