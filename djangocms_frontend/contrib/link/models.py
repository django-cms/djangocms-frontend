from django.utils.translation import gettext as _

from djangocms_frontend.contrib.link.helpers import GetLinkMixin

# 'link' type is added manually as it is only required for this plugin
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES

COLOR_STYLE_CHOICES = (("link", _("Link")),) + COLOR_STYLE_CHOICES


class Link(GetLinkMixin, FrontendUIItem):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    class Meta:
        proxy = True
        verbose_name = _("Link")

    def get_short_description(self):
        if self.config.get("name", "") and self.get_link():
            return f"{self.name} ({self.get_link()})"
        return self.config.get("name", "") or self.get_link() or _("<link is missing>")
