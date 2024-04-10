from django.utils.translation import gettext_lazy as _

from ...models import FrontendUIItem


class Tab(FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Tab")

    def get_short_description(self):
        text = f"({self.tab_type})"

        if self.tab_alignment:
            text += f" .{self.tab_alignment}"
        return text


class TabItem(FrontendUIItem):
    """
    Components > "Navs - Tab Item" Plugin
    https://getbootstrap.com/docs/5.0/components/navs/
    """

    class Meta:
        proxy = True
        verbose_name = _("Tab item")

    def get_short_description(self):
        return self.tab_title
