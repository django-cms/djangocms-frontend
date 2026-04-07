from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem

from .conf import ICON_TAG_TYPES


class Icon(FrontendUIItem):
    """
    Adds icons from configurable icon picker
    https://github.com/migliori/universal-icon-picker
    """

    class Meta:
        proxy = True
        verbose_name = _("Icon")

    default_tag_type = first_choice(ICON_TAG_TYPES)

    def get_short_description(self):
        return self.config.get("icon", {}).get("iconClass", _("undefined"))
