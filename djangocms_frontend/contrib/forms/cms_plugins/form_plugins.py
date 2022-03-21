from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.contrib.forms import forms, models

from .. import forms as forms_module
from .ajax_plugins import FormPlugin

mixin_factory = settings.get_renderer(forms_module)


class FormElementPlugin(CMSUIPlugin):
    top_element = FormPlugin.__name__
    module = _("Forms")
    render_template = f"djangocms_frontend/{settings.framework}/widgets/base.html"

    @classmethod
    def get_parent_classes(cls, slot, page, instance=None):
        """Only valid as indirect child of the cls.top_element"""
        if instance is None:
            return [""]
        parent = instance
        while parent is not None:
            if parent.plugin_type == cls.top_element:
                return super().get_parent_classes(slot, page, instance)
            parent = parent.parent
        return [""]

    def render(self, context, instance, placeholder):
        instance.add_classes("form-control")
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CharFieldPlugin(FormElementPlugin):
    name = _("Text line")
    model = models.CharField
    form = forms.CharFieldForm


@plugin_pool.register_plugin
class TextareaPlugin(FormElementPlugin):
    name = _("Text area")
    model = models.TextareaField
    form = forms.TextareaFieldForm


@plugin_pool.register_plugin
class SelectPlugin(FormElementPlugin):
    name = _("Select field")
    model = models.Select
    form = forms.SelectFieldForm


@plugin_pool.register_plugin
class BooleanFieldPlugin(FormElementPlugin):
    name = _("Boolean field")
    model = models.BooleanField
    form = forms.BooleanFieldForm
