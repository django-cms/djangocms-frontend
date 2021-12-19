from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_icon.fields import Icon
from djangocms_link.models import AbstractLink

from djangocms_frontend.settings import COLOR_STYLE_CHOICES

# 'link' type is added manually as it is only required for this plugin
from ...models import FrontendUIItem
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES

COLOR_STYLE_CHOICES = (("link", _("Link")),) + COLOR_STYLE_CHOICES


class Link(FrontendUIItem):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    class Meta:
        proxy = True
