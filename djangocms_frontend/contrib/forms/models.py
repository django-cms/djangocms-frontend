from django.utils.translation import gettext as _

from djangocms_frontend.models import FrontendUIItem


class Form(FrontendUIItem):
    class Meta:
        proxy = True
        verbose_name = _("Form")
