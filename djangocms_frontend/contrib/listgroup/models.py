from ...models import FrontendUIItem
from .constants import LISTGROUP_STATE_CHOICES


class ListGroup(FrontendUIItem):
    """
    Components > "List Group" Plugin
    https://getbootstrap.com/docs/5.0/components/list-group/
    """

    class Meta:
        proxy = True

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

    def get_short_description(self):
        text = []
        if self.list_context:
            text.append(".list-group-item-{}".format(self.list_context))
        if self.list_state:
            text.append(".{}".format(self.list_state))
        return " ".join(text)
