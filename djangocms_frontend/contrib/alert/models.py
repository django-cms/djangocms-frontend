from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Alert(FrontendUIItem):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        proxy = True
        verbose_name = _("Alert")

    def get_short_description(self):
        return f"({self.alert_context})"
