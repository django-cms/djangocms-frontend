from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from djangocms_frontend.helpers import get_related_object


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


class GetLinkMixin:
    def get_link(self) -> str:
        if "url_grouper" in self.config and self.config["url_grouper"] and apps.is_installed("djangocms_url_manager"):
            url_grouper = get_related_object(self.config, "url_grouper")
            if not url_grouper:
                return ""
            from djangocms_url_manager.models import Url

            url = Url.objects.filter(url_grouper=url_grouper).order_by("pk").last()
            if not url:  # pragma: no cover
                return ""
            return url.get_absolute_url() or ""

        from djangocms_link.helpers import get_link as djangocms_link_get_link

        return djangocms_link_get_link(self.config.get("link", {}), Site.objects.get_current().pk) or ""
