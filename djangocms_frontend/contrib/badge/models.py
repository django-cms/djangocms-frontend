from djangocms_frontend.models import FrontendUIItem


class Badge(FrontendUIItem):
    """
    Components > "Badge" Plugin
    https://getbootstrap.com/docs/5.0/components/badge/
    """

    class Meta:
        proxy = True

    def get_short_description(self):
        return "({})".format(self.badge_context)
