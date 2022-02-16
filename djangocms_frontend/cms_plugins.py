from cms.plugin_base import CMSPluginBase


class CMSUIPlugin(CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"
