from django.utils.translation import gettext_lazy as _

MODAL_CENTERED_CHOICES = (
    ("modal-dialog-centered", _("Vertically centered")),
    ("modal-dialog-centered modal-dialog-scrollable", _("Vertically centered scrollable")),
)

MODAL_SIZE_CHOICES = (
    ("modal-sm", _("Small")),
    ("modal-lg", _("Large")),
    ("modal-xl", _("Extra Large")),
)

MODAL_FULLSCREEN_CHOICES = (
        ("modal-fullscreen", _("Allways")),
        ("modal-fullscreen-sm-down", _("Fullscreen below sm")),
        ("modal-fullscreen-md-down", _("Fullscreen below md")),
        ("modal-fullscreen-lg-down", _("Fullscreen below lg")),
        ("modal-fullscreen-xl-down", _("Fullscreen below xl")),
        ("modal-fullscreen-xxl-down", _("Fullscreen below xxl")),
)

MODAL_INNER_TYPE_CHOICES = (
    ("modal-body", _("Body")),
    ("modal-header", _("Header")),
)
