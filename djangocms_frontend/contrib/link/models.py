from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext as _

from djangocms_frontend.helpers import get_related_object

# 'link' type is added manually as it is only required for this plugin
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES

COLOR_STYLE_CHOICES = (("link", _("Link")),) + COLOR_STYLE_CHOICES


class GetLinkMixin:
    def get_link(self):
        if getattr(self, "url_grouper", None):
            url_grouper = get_related_object(self.config, "url_grouper")
            if not url_grouper:
                return ""
            url = url_grouper.get_content(show_draft_content=True)
            # simulate the call to the unauthorized CMSPlugin.page property
            cms_page = self.placeholder.page if self.placeholder_id else None

            # first, we check if the placeholder the plugin is attached to
            # has a page. Thus the check "is not None":
            if cms_page is not None:
                if getattr(cms_page, "node", None):
                    cms_page_site_id = getattr(cms_page.node, "site_id", None)
                else:
                    cms_page_site_id = getattr(cms_page, "site_id", None)
            # a plugin might not be attached to a page and thus has no site
            # associated with it. This also applies to plugins inside
            # static placeholders
            else:
                cms_page_site_id = None
            return url.get_url(cms_page_site_id) or ""

        if getattr(self, "internal_link", None):
            try:
                ref_page = get_related_object(self.config, "internal_link")
                link = ref_page.get_absolute_url()
            except (
                KeyError,
                TypeError,
                ValueError,
                AttributeError,
                models.ObjectDoesNotExist,
            ):
                self.internal_link = None
                return ""

            # simulate the call to the unauthorized CMSPlugin.page property
            cms_page = self.placeholder.page if self.placeholder_id else None

            # first, we check if the placeholder the plugin is attached to
            # has a page. Thus, the check "is not None":
            if cms_page is not None:
                if getattr(cms_page, "node", None):
                    cms_page_site_id = getattr(cms_page.node, "site_id", None)
                else:
                    cms_page_site_id = getattr(cms_page, "site_id", None)
            # a plugin might not be attached to a page and thus has no site
            # associated with it. This also applies to plugins inside
            # static placeholders
            else:
                cms_page_site_id = None

            # now we do the same for the reference page the plugin links to
            # in order to compare them later
            if getattr(ref_page, "node", None):
                ref_page_site_id = ref_page.node.site_id
            elif getattr(ref_page, "site_id", None):
                ref_page_site_id = ref_page.site_id
            # if no external reference is found the plugin links to the
            # current page
            else:
                ref_page_site_id = Site.objects.get_current().pk

            if ref_page_site_id != cms_page_site_id:
                ref_site = Site.objects._get_site_by_id(ref_page_site_id).domain
                link = f"//{ref_site}{link}"

        elif getattr(self, "file_link", None):
            link = getattr(get_related_object(self.config, "file_link"), "url", "")

        elif getattr(self, "external_link", None):
            link = self.external_link

        elif getattr(self, "phone", None):
            link = "tel:{}".format(self.phone.replace(" ", ""))

        elif getattr(self, "mailto", None):
            link = f"mailto:{self.mailto}"

        else:
            link = ""

        if (not getattr(self, "phone", None) and not getattr(self, "mailto", None)) and getattr(self, "anchor", None):
            link += f"#{self.anchor}"

        return link


class Link(GetLinkMixin, FrontendUIItem):
    """
    Components > "Button" Plugin
    https://getbootstrap.com/docs/5.0/components/buttons/
    """

    class Meta:
        proxy = True
        verbose_name = _("Link")

    def get_short_description(self):
        if self.config.get("name", "") and self.get_link():
            return f"{self.name} ({self.get_link()})"
        return self.config.get("name", "") or self.get_link() or _("<link is missing>")
