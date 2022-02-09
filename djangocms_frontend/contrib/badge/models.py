from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Badge(FrontendUIItem):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    class Meta:
        proxy = True
        verbose_name = _("Badge")

    def get_short_description(self):
        return f"({self.badge_context})"
