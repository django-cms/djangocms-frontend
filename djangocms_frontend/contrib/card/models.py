from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES

# card allow for a transparent color
CARD_COLOR_STYLE_CHOICES = COLOR_STYLE_CHOICES + (("transparent", _("Transparent")),)

CARD_TEXT_STYLES = COLOR_STYLE_CHOICES + (("white", _("White")),)


class CardLayout(FrontendUIItem):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        text = "({})".format(self.card_type)
        return text


class Card(FrontendUIItem):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        if self.card_context and self.card_outline:
            text = ".border-{}".format(self.card_context)
        elif self.card_context:
            text = ".bg-{}".format(self.card_context)
        else:
            text = ""
        if self.card_alignment:
            text += " .{}".format(self.card_alignment)
        return text


class CardInner(FrontendUIItem):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return "({})".format(self.inner_type.split("-", 1)[-1])
