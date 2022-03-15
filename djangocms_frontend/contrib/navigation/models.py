from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Navigation(FrontendUIItem):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        proxy = True
        verbose_name = _("Navigation")

    def get_short_description(self):
        return f'({self.config.get("navbar_design", "-")})'


class PageTree(FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Page tree")


class Brand(FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Brand")
