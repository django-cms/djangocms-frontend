from cms.constants import SLUG_REGEXP
from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_str

from djangocms_frontend.helpers import get_related

if hasattr(CMSPluginBase, "edit_field"):
    # FrontendEditable functionality already implemented in core?
    FrontendEditableAdminMixin = object
else:
    # If not use our own version of the plugin-enabled mixin
    from .helpers import FrontendEditableAdminMixin


class CMSUIPlugin(FrontendEditableAdminMixin, CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_str(super().__str__())

    def render(self, context, instance, placeholder):
        for key, value in instance.config.items():
            if isinstance(value, dict) and set(value.keys()) == {"pk", "model"}:
                if key not in instance.__dir__():  # hasattr would return the value in the config dict
                    setattr(instance.__class__, key, get_related(key))
        return super().render(context, instance, placeholder)

    def get_plugin_urls(self):
        from django.urls import re_path

        info = f"{self.model._meta.app_label}_{self.model._meta.model_name}"

        def pat(regex, fn):
            return re_path(regex, fn, name=f"{info}_{fn.__name__}")

        return [
            pat(r'edit-field/(%s)/([a-z\-]+)/$' % SLUG_REGEXP, self.edit_field),
        ]

    def _get_object_for_single_field(self, object_id, language):
        from .models import FrontendUIItem

        return FrontendUIItem.objects.get(pk=object_id)
