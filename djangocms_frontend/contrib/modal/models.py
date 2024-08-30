from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem

# TODO leaving this comment for now
# data-bs-toggle="modal" data-bs-target="#modalExample"
# aria-expanded="false" aria-controls="modalExample">
# data-bs-target can also be classes
# data-bs-parent links to the wrapper modal
# <div class="modal" id="modalExample">


class Modal(FrontendUIItem):
    """
    Component > "Modal" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        proxy = True
        verbose_name = _("Modal")

    def get_short_description(self):
        return f"(modal-{str(self.pk)})"


class ModalTrigger(FrontendUIItem):
    """
    Component > "Modal Trigger" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        proxy = True
        verbose_name = _("Modal trigger")

    def get_short_description(self):
        return f"({self.trigger_identifier})"


class ModalContainer(FrontendUIItem):
    """
    Component > "Modal Container" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        proxy = True
        verbose_name = _("Modal container")

    def get_short_description(self):
        return f"({self.container_identifier})"

class ModalInner(FrontendUIItem):
    """
    Component > "Modal Inner" Plugin
    https://getbootstrap.com/docs/5.0/components/modal/
    """

    class Meta:
        proxy = True
        verbose_name = _("Modal inner")

    def get_short_description(self):
        return f"({self.inner_type})"