from importlib import import_module

from cms.forms.utils import get_page_choices
from cms.models import Page
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.utils.encoding import force_text
from django.utils.html import mark_safe

LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])


def create_querysets(link_models):
    querysets = []
    for item in LINK_MODELS:
        if item["class_path"] != "cms.models.Page":
            # CMS pages are collected using a cms function to preserve hierarchy
            section = item["type"]
            parts = item["class_path"].rsplit(".", 1)
            cls = getattr(import_module(parts[0]), parts[1])
            queryset = cls.objects

            if "manager_method" in item:
                queryset = getattr(queryset, item["manager_method"])()

            if "filter" in item:
                for (k, v) in item["filter"].items():
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
            querysets.append((section, queryset, item.get("search", None)))
    return querysets


_querysets = create_querysets(LINK_MODELS)


def get_link_choices(term="", lang=None, nbsp=""):
    global _querysets

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
                            text=mark_safe(name.replace("&nbsp;", nbsp)),
                        )
                        for page, name in descr
                        if not isinstance(term, str) or term.upper() in name.upper()
                    ],
                }
            )
        elif value and isinstance(value, int):
            available_objects.append(dict(id=f"{type_id}-{value}"))

    # Add list of additional non-cms pages
    for section, qs, search in _querysets:
        objects = None
        if search:
            try:
                objects = qs.filter(**{search: term})
                print(objects)
            except FieldError:
                pass
        if objects is None:
            objects = [
                item
                for item in qs.all()
                if (not isinstance(term, str)) or term.upper() in str(item).upper()
            ]
        if objects:
            type_class = ContentType.objects.get_for_model(objects[0].__class__)
            available_objects.append(
                {
                    "text": force_text(section),
                    "children": [
                        dict(id=f"{type_class.id}-{obj.id}", text=str(obj))
                        for obj in objects
                    ],
                }
            )
    return available_objects


def get_choices(term="", lang=None):
    def to_choices(json):
        return list(
            (elem["text"], to_choices(elem["children"]))
            if "children" in elem
            else (elem["id"], elem["text"])
            for elem in json
        )

    return to_choices(get_link_choices(term, lang, "&nbsp;"))
