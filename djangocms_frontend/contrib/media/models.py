from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Media(FrontendUIItem):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        proxy = True
        verbose_name = _("Media")

    def get_short_description(self):
        return ""


class MediaBody(FrontendUIItem):
    """
    Layout > "Media body" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        proxy = True
        verbose_name = _("Media body")

    def get_short_description(self):
        return ""
