from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem

# TODO leaving this comment for now
# data-bs-toggle="collapse" data-bs-target="#collapseExample"
# aria-expanded="false" aria-controls="collapseExample">
# data-bs-target can also be classes
# data-bs-parent links to the wrapper collapse
# <div class="collapse" id="collapseExample">


class Collapse(FrontendUIItem):
    """
    Component > "Collapse" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        proxy = True
        verbose_name = _("Collapse")

    def get_short_description(self):
        return f"(collapse-{str(self.pk)})"


class CollapseTrigger(FrontendUIItem):
    """
    Component > "Collapse Trigger" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        proxy = True
        verbose_name = _("Collapse trigger")

    def get_short_description(self):
        return f"({self.trigger_identifier})"


class CollapseContainer(FrontendUIItem):
    """
    Component > "Collapse Container" Plugin
    https://getbootstrap.com/docs/5.0/components/collapse/
    """

    class Meta:
        proxy = True
        verbose_name = _("Collapse container")

    def get_short_description(self):
        return f"({self.container_identifier})"
