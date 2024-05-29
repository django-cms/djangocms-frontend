from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_str

from djangocms_frontend.helpers import get_related_object


class CMSUIPlugin(CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_str(super().__str__())

    def render(self, context, instance, placeholder):
        for key, value in instance.config.items():
            if isinstance(value, dict) and set(value.keys()) == {"pk", "model"}:
                if not hasattr(instance, key + "_related"):
                    setattr(instance, key + "_related", get_related_object(instance.config, key))
        return super().render(context, instance, placeholder)
