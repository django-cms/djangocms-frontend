from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, BackgroundMixin, ResponsiveMixin, SpacingMixin
from ...helpers import get_plugin_template
from .. import jumbotron
from . import forms, models

mixin_factory = settings.get_renderer(jumbotron)


@plugin_pool.register_plugin
class JumbotronPlugin(
    mixin_factory("Jumbotron"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.1/examples/jumbotron/
    """

    name = _("Jumbotron")
    module = _("Frontend")
    model = models.Jumbotron
    form = forms.JumbotronForm
    change_form_template = "djangocms_frontend/admin/jumbotron.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "template",
                    "jumbotron_fluid",
                )
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(instance, "jumbotron", "jumbotron", settings.JUMBOTRON_TEMPLATE_CHOICES)
