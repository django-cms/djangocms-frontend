from importlib import import_module

from cms.forms.utils import get_page_choices
from cms.models import Page
from django.apps import apps
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.http import Http404, JsonResponse
from django.views.generic import View

LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])


def get_link_choices(lang=None):
    available_objects = []

    for item in LINK_MODELS:
        if item["class_path"] != "cms.models.Page":
            # CMS pages are collected using a cms function to preserve hierarchy
            model = item["type"]
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

            available_objects.append(
                {
                    "model": model,
                    "objects": list(queryset),
                }
            )

    # Now create our list of choices for the <select> field
    object_choices = []
    type_id = ContentType.objects.get_for_model(Page).id
    for value, descr in get_page_choices(lang):
        if isinstance(descr, list):
            hierarchy = []
            for page, name in descr:
                hierarchy.append((f"{type_id}-{page}", name))
            object_choices.append((value, hierarchy))
        else:
            object_choices.append((value, descr))

    for group in available_objects:
        obj_list = []
        for obj in group["objects"]:
            type_class = ContentType.objects.get_for_model(obj.__class__)
            form_value = f"{type_class.id}-{obj.id}"
            display_text = str(obj)

            obj_list.append((form_value, display_text))
        object_choices.append(
            (
                group["model"],
                obj_list,
            )
        )
    return object_choices


class AutocompleteJsonView(View):
    """Handle AutocompleteWidget's AJAX requests for data."""

    paginate_by = 20
    admin_site = None

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """
        return JsonResponse(
            {
                "results": get_link_choices(),
                "pagination": {"more": False},
            }
        )

    def get_paginator(self, *args, **kwargs):
        """Use the ModelAdmin's paginator."""
        return self.model_admin.get_paginator(self.request, *args, **kwargs)

    def get_queryset(self):
        """Return queryset based on ModelAdmin.get_search_results()."""
        qs = self.model_admin.get_queryset(self.request)
        qs = qs.complex_filter(self.source_field.get_limit_choices_to())
        qs, search_use_distinct = self.model_admin.get_search_results(
            self.request, qs, self.term
        )
        if search_use_distinct:
            qs = qs.distinct()
        return qs

    def process_request(self, request):
        """
        Validate request integrity, extract and return request parameters.

        Since the subsequent view permission check requires the target model
        admin, which is determined here, raise PermissionDenied if the
        requested app, model or field are malformed.

        Raise Http404 if the target model admin is not configured properly with
        search_fields.
        """
        term = request.GET.get("term", "")
        try:
            app_label = request.GET["app_label"]
            model_name = request.GET["model_name"]
            field_name = request.GET["field_name"]
        except KeyError as e:
            raise PermissionDenied from e

        # Retrieve objects from parameters.
        try:
            source_model = apps.get_model(app_label, model_name)
        except LookupError as e:
            raise PermissionDenied from e

        try:
            source_field = source_model._meta.get_field(field_name)
        except FieldDoesNotExist as e:
            raise PermissionDenied from e
        try:
            remote_model = source_field.remote_field.model
        except AttributeError as e:
            raise PermissionDenied from e
        try:
            model_admin = self.admin_site._registry[remote_model]
        except KeyError as e:
            raise PermissionDenied from e

        # Validate suitability of objects.
        if not model_admin.get_search_fields(request):
            raise Http404(
                "%s must have search_fields for the autocomplete_view."
                % type(model_admin).__qualname__
            )

        to_field_name = getattr(
            source_field.remote_field, "field_name", remote_model._meta.pk.attname
        )
        to_field_name = remote_model._meta.get_field(to_field_name).attname
        if not model_admin.to_field_allowed(request, to_field_name):
            raise PermissionDenied

        return term, model_admin, source_field, to_field_name

    def has_perm(self, request, obj=None):
        """Check if user has permission to access the related model."""
        return self.model_admin.has_view_permission(request, obj=obj)
