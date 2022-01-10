from ...models import FrontendUIItem


class CodeBlock(FrontendUIItem):
    """
    Content > "Code" Plugin
    https://getbootstrap.com/docs/5.0/content/code/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return "<{}>".format(self.code_type)


class Blockquote(FrontendUIItem):
    """
    Content > "Blockquote" Plugin
    https://getbootstrap.com/docs/5.0/content/typography/#blockquotes
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return self.quote_content


class Figure(FrontendUIItem):
    """
    Content > "Figure" Plugin
    https://getbootstrap.com/docs/5.0/content/figures/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return self.figure_caption
