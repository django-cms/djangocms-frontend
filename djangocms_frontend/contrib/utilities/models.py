from django.utils.translation import gettext_lazy as _

from ...models import FrontendUIItem


class Spacing(FrontendUIItem):
    """
    Utilities > "Spacing" Plugin
    https://getbootstrap.com/docs/5.0/utilities/spacing/
    """

    class Meta:
        proxy = True
        verbose_name = _("Spacing")

    def get_base_css_class(self):
        # Source: https://getbootstrap.com/docs/5.0/utilities/spacing/#notation
        # [...] format {property}{sides}-{size} for xs and
        # {property}{sides}-{breakpoint}-{size} for sm, md, lg, and xl.

        prop = self.get_framework_value("space_property")
        side = self.get_framework_value("space_sides")
        device = self.get_framework_value("space_device")
        size = self.get_framework_value("space_size")
        if not prop or size in ("", None):
            return ""
        return f"{prop}{side}-{size}" if not device or device == "xs" else f"{prop}{side}-{device}-{size}"

    def get_short_description(self):
        css_class = self.get_base_css_class()
        return f"(.{css_class})" if css_class else ""


class Heading(FrontendUIItem):
    """
    Creates a heading (<h1>, <h2>, ...) and adds the entry to the table of contents (if an id is given)
    """

    class Meta:
        proxy = True
        verbose_name = _("Heading")

    def get_short_description(self):
        return f"({self.heading})"


class TableOfContents(FrontendUIItem):
    """
    Creates a table of contents of all headings processed BEFORE the plugin.
    If the table of contents is supposed to be at the top of the page, move the surrounding column
    using flexbox directives.
    """

    class Meta:
        proxy = True
        verbose_name = _("Table of contents")

    def get_short_description(self):
        return f"({self.id})"
