from django.utils.translation import gettext_lazy as _

CARD_LAYOUT_TYPE_CHOICES = (
    ("card-group", _("Card group")),
    ("row", _("Grid cards")),  # Removed in 5
)

CARD_ALIGNMENT_CHOICES = (
    ("start", _("Left")),
    ("center", _("Center")),
    ("end", _("Right")),
)

CARD_INNER_TYPE_CHOICES = (
    ("card-body", _("Body")),
    ("card-header", _("Header")),
    ("card-footer", _("Footer")),
    ("card-img-overlay", _("Image overlay")),
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
