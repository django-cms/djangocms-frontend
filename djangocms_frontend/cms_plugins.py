import uuid

from cms.constants import SLUG_REGEXP
from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_str

from djangocms_frontend.helpers import get_related_object

from .helpers import FrontendEditableAdminMixin


def _get_related(instance, key):
    def get_related():
        obj = get_related_object(instance.config, key)
        setattr(instance, key, obj)
        return obj
    get_related.__name__ = key
    return get_related


class CMSUIPlugin(FrontendEditableAdminMixin, CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_str(super().__str__())

    def render(self, context, instance, placeholder):
        for key, value in instance.config.items():
            if isinstance(value, dict) and set(value.keys()) == {"pk", "model"}:
                if key not in instance.__dir__():  # hasattr would return the value in the config dict
                    setattr(instance, key, _get_related(instance, key))
        instance.uuid = str(uuid.uuid4())
        return super().render(context, instance, placeholder)

    def get_plugin_urls(self):
        from django.urls import re_path

        info = f"{self.model._meta.app_label}_{self.model._meta.model_name}"
        pat = lambda regex, fn: re_path(regex, fn, name=f"{info}_{fn.__name__}")

        return [
            pat(r'edit-field/(%s)/([a-z\-]+)/$' % SLUG_REGEXP, self.edit_field),
        ]

    def _get_object_for_single_field(self, object_id, language):
        from .models import FrontendUIItem

        return FrontendUIItem.objects.get(pk=object_id)
