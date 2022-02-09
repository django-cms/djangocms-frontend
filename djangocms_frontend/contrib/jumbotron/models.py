from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class Jumbotron(FrontendUIItem):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    class Meta:
        proxy = True
        verbose_name = _("Jumbotron")

    def get_short_description(self):
        text = ""
        if self.jumbotron_fluid:
            text = "({})".format(_("Fluid"))
        return text
