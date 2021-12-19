from djangocms_frontend.models import FrontendUIItem


class Alert(FrontendUIItem):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return "({})".format(self.alert_context)
