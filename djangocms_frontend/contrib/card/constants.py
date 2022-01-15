from django.utils.translation import gettext_lazy as _

CARD_TYPE_CHOICES = (
    ("card", _("Card")),
    ("card-group", _("Card group")),
    ("row", _("Card deck v4 (deprecated)")),  # Removed in 5
    ("card-masonry", _("Card masonry")),  # Removed in 5
)

CARD_ALIGNMENT_CHOICES = (
    ("text-left", _("Left")),
    ("text-center", _("Center")),
    ("text-right", _("Right")),
)

CARD_INNER_TYPE_CHOICES = (
    ("card-body", _("Body")),
    ("card-header", _("Header")),
    ("card-footer", _("Footer")),
)

CARD_TAG_CHOICES = (
    ("div", "DIV"),
    ("h1", "H1"),
    ("h2", "H2"),
    ("h3", "H3"),
    ("h4", "H4"),
    ("h5", "H5"),
    ("h6", "H6"),
    ("p", "P"),
    ("small", "SMALL"),
)
