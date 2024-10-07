from importlib import import_module

from cms.forms.utils import get_page_choices
from cms.models import Page
from django.conf import settings as django_settings
from django.contrib.admin import site
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.utils.encoding import force_str

from djangocms_frontend.helpers import get_related_object

LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])


def create_querysets(link_models):
    querysets = []
    for item in link_models:
        if item["class_path"] != "cms.models.Page":
            # CMS pages are collected using a cms function to preserve hierarchy
            section = item["type"]
            parts = item["class_path"].rsplit(".", 1)
            cls = getattr(import_module(parts[0]), parts[1])
            queryset = cls.objects

            if "manager_method" in item:
                queryset = getattr(queryset, item["manager_method"])()

            if "filter" in item:
                for k, v in item["filter"].items():
                    try:
                        # Attempt to execute any callables in the filter dict.
                        item["filter"][k] = v()
                    except TypeError:
                        # OK, it wasn't a callable, so, leave it be
                        pass
                queryset = queryset.filter(**item["filter"])
            else:
                if "manager_method" not in item:
                    queryset = queryset.all()
            if "order_by" in item:
                queryset = queryset.order_by(item["order_by"])
            querysets.append((section, queryset, item.get("search", None), cls))
    return querysets


_querysets = create_querysets(LINK_MODELS)


def get_object_for_value(value):
    if isinstance(value, str) and "-" in value:
        type_id, obj_id = value.split("-", 1)
        try:
            content_type = ContentType.objects.get(id=type_id)
            return dict(
                model=f"{content_type.app_label}.{content_type.model}",
                pk=int(obj_id),
            )
        except (ObjectDoesNotExist, TypeError):
            pass
    return None


def unescape(text, nbsp):
    return (
        text.replace("&nbsp;", nbsp)
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#x27;", "'")
    )


def get_link_choices(request, term="", lang=None, nbsp=None):
    global _querysets

    if nbsp is None:
        nbsp = "" if term else "\u2000"
    available_objects = []
    # Now create our list of cms pages
    type_id = ContentType.objects.get_for_model(Page).id
    for value, descr in get_page_choices(lang):
        if isinstance(descr, list):
            available_objects.append(
                {
                    "text": value,
                    "children": [
                        dict(
                            id=f"{type_id}-{page}",
                            # django admin's autocomplete view requires unescaped strings
                            # get_page_choices escapes strings, so we undo the escape
                            text=unescape(name, nbsp),
                        )
                        for page, name in descr
                        if not isinstance(term, str) or term.upper() in name.upper()
                    ],
                }
            )
        elif value and isinstance(value, int):
            available_objects.append(dict(id=f"{type_id}-{value}"))

    # Add list of additional non-cms pages
    for section, qs, search, cls in _querysets:
        objects = None
        model_admin = site._registry.get(cls, None)
        if search:
            try:
                objects = qs.filter(**{search + "__icontains": term})
            except FieldError:
                pass
        if objects is None:
            objects = [item for item in qs.all() if (not isinstance(term, str)) or term.upper() in str(item).upper()]
        if objects:
            type_class = ContentType.objects.get_for_model(objects[0].__class__)
            available_objects.append(
                {
                    "text": force_str(section),
                    "children": [
                        dict(id=f"{type_class.id}-{obj.id}", text=str(obj))
                        for obj in objects
                        if request is None or model_admin and model_admin.has_view_permission(request, obj=obj)
                    ],
                }
            )
    return available_objects


def get_choices(request, term="", lang=None) -> list:
    def to_choices(json):
        return list(
            (elem["text"], to_choices(elem["children"])) if "children" in elem else (elem["id"], elem["text"])
            for elem in json
        )

    return to_choices(get_link_choices(request, term, lang, "&nbsp;"))


class GetLinkMixin:
    def __init__(self, *args, **kwargs):
        self._cms_page = None
        super().__init__(*args, **kwargs)

    def get_link(self):
        if getattr(self, "url_grouper", None):
            url_grouper = get_related_object(self.config, "url_grouper")
            if not url_grouper:
                return ""
            # The next line is a workaround, since djangocms-url-manager does not provide a way of
            # getting the current URL object.
            from djangocms_url_manager.models import Url
            url = Url._base_manager.filter(url_grouper=url_grouper).order_by("pk").last()
            if not url:  # pragma: no cover
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
                ObjectDoesNotExist,
            ):
                self.internal_link = None
                return ""

            # simulate the call to the unauthorized CMSPlugin.page property
            cms_page = self._cms_page or self.placeholder.page if self.placeholder_id else None

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
