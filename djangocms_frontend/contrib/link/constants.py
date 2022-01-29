from django.conf import settings
from django.utils.translation import gettext_lazy as _

LINK_CHOICES = (
    ("link", _("Link")),
    ("btn", _("Button")),
)

LINK_SIZE_CHOICES = (
    ("btn-sm", _("Small")),
    ("", _("Medium")),
    ("btn-lg", _("Large")),
)

USE_LINK_ICONS = getattr(
    settings,
    "DJANGOCMS_BOOTSTRAP5_USE_ICONS",
    True,
)

TARGET_CHOICES = (
    ("_blank", _("Open in new window")),
    ("_self", _("Open in same window")),
    ("_parent", _("Delegate to parent")),
    ("_top", _("Delegate to top")),
)
