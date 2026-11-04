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
        verbose_name = _("Card layout")

    def get_short_description(self):
        text = f"({self.get_framework_value('card_type')})"
        return text


class Card(FrontendUIItem):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        proxy = True
        verbose_name = _("Card")

    def get_short_description(self):
        background = self.get_framework_value("background_context")
        if background:
            text = [f".bg-{background}"]
        else:
            text = []
        outline = self.get_framework_value("card_outline")
        if outline:
            text.append(f".border-{outline}")
        if self.card_alignment:
            text.append(f".{self.card_alignment}")
        return " ".join(text)


class CardInner(FrontendUIItem):
    """
    Components > "Card - Inner" Plugin (Header, Footer, Body)
    https://getbootstrap.com/docs/5.0/components/card/
    """

    class Meta:
        proxy = True
        verbose_name = _("Card inner")

    def get_short_description(self):
        return "({})".format(self.get_framework_value("inner_type").split("-", 1)[-1])
