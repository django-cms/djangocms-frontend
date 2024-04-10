from django.utils.translation import gettext_lazy as _

from ...models import FrontendUIItem


class ListGroup(FrontendUIItem):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        proxy = True
        verbose_name = _("List group")

    def get_short_description(self):
        text = ""
        if self.list_group_flush:
            text += ".list-group-flush"
        return text


class ListGroupItem(FrontendUIItem):
    """
    Components > "List Group Ite" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        proxy = True
        verbose_name = _("List group item")

    def get_short_description(self):
        text = []
        if self.list_context:
            text.append(f".list-group-item-{self.list_context}")
        if self.list_state:
            text.append(f".{self.list_state}")
        return " ".join(text)
