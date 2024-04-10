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

        if not self.space_device or self.space_device == "xs":
            template = "{property}{sides}-{size}"
        else:
            template = "{property}{sides}-{breakpoint}-{size}"

        return template.format(
            property=self.space_property,
            sides=self.space_sides,
            breakpoint=self.space_device,
            size=self.space_size,
        )

    def get_short_description(self):
        return f"(.{self.get_base_css_class()})"


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
