# Import the components from the current directory's models module
from cms.plugin_base import CMSPluginBase
from django.utils.encoding import force_str

from djangocms_frontend.helpers import get_related
from djangocms_frontend.models import AbstractFrontendUIItem

try:
    from cms.admin.placeholderadmin import PlaceholderAdmin

    if hasattr(PlaceholderAdmin, "edit_field"):
        # FrontendEditable functionality already implemented in core?
        class FrontendEditableAdminMixin:
            pass
    else:
        # If not use our own version of the plugin-enabled mixin
        raise ImportError
except ImportError:
    # django CMS 3 did not implement this: use our own version of the plugin-enabled mixin
    from .helpers import FrontendEditableAdminMixin

    class PlaceholderAdmin:
        pass


class CMSUIPluginBase(FrontendEditableAdminMixin, CMSPluginBase):
    render_template = "djangocms_frontend/html_container.html"
    change_form_template = "djangocms_frontend/admin/base.html"

    def __str__(self):
        return force_str(super().__str__())

    def render(self, context, instance, placeholder):
        if isinstance(instance, AbstractFrontendUIItem):
            for key, value in instance.config.items():
                if isinstance(value, dict) and set(value.keys()) == {"pk", "model"}:
                    if key not in instance.__dir__():  # hasattr would return the value in the config dict
                        setattr(instance.__class__, key, get_related(key))
            if "instance" not in instance.config and isinstance(instance.config, dict):
                context.update(instance.config)
        return super().render(context, instance, placeholder)

    if not hasattr(PlaceholderAdmin, "edit_field"):
        # If the PlaceholderAdmin does not have the edit_field method, we need to provide
        # the urls and the object getter here
        def get_plugin_urls(self):
            from django.urls import re_path

            info = f"{self.model._meta.app_label}_{self.model._meta.model_name}"

            def pat(regex, fn):
                return re_path(regex, fn, name=f"{info}_{fn.__name__}")

            return [
                pat(r"edit-field/([0-9]+)/([a-z\-]+)/$", self.edit_field),
            ] + super().get_plugin_urls()

        def _get_object_for_single_field(self, object_id, language):
            # Method to get the object for the single field edit view
            from .models import FrontendUIItem

            return FrontendUIItem.objects.get(pk=object_id)


class CMSUIComponent(CMSUIPluginBase):
    pass
