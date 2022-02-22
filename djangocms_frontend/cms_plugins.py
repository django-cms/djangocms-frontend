from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_text


class CMSUIPlugin(CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_text(super().__str__())
