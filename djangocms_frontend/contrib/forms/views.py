import hashlib

from cms.models import CMSPlugin
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.views import View

_formview_pool = {}


def register_form_view(cls, slug=None):
    """
    Registers a Widget (with type defined by cls) and slug
    :type cls: class
    :type slug: string to instantiate dashboard_widget
    """
    if not slug:
        slug = get_random_string(length=12)
    key = hashlib.sha384(slug.encode("utf-8")).hexdigest()
    if key in _formview_pool:
        assert _formview_pool[key][0] == cls, _(
            "Only unique slugs accepted for form views"
        )
    _formview_pool[key] = (cls, slug, key)
    return key


class AjaxView(View):
    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.method == "GET" and "get" in self.http_method_names:
                return self.ajax_get(request, *args, **kwargs)
            elif request.method == "POST" and "post" in self.http_method_names:
                return self.ajax_post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def decode_path(path):
        params = {}
        for element in path.split(","):
            if "=" in element:
                params[element.split("=", 1)[0]] = element.split("=", 1)[1]
            elif "%3D" in element:
                params[element.split("%3D", 1)[0]] = element.split("%3D", 1)[1]
            else:
                params[element] = True
        return params

    @staticmethod
    def plugin_instance(pk):
        plugin = get_object_or_404(CMSPlugin, pk=pk)
        plugin.__class__ = plugin.get_plugin_class()
        instance = (
            plugin.model.objects.get(cmsplugin_ptr=plugin.id)
            if hasattr(plugin.model, "cmsplugin_ptr")
            else plugin
        )
        return plugin, instance

    def ajax_post(self, request, *args, **kwargs):
        if "instance_id" in kwargs:
            plugin, instance = self.plugin_instance(kwargs["instance_id"])
            if hasattr(plugin, "ajax_post"):
                request.POST = QueryDict(request.body)
                try:
                    params = (
                        self.decode_path(kwargs["parameter"])
                        if "parameter" in kwargs
                        else {}
                    )
                    return plugin.ajax_post(request, instance, params)
                except ValidationError as error:
                    return JsonResponse({"result": "error", "msg": str(error.args[0])})
            else:
                raise Http404()
        elif "form_id" in kwargs:
            if kwargs["form_id"] in _formview_pool:
                form_id = kwargs.pop("form_id")
                instance = _formview_pool[form_id][0](*args, **kwargs)
                if hasattr(instance, "ajax_post"):
                    return instance.ajax_post(request, *args, **kwargs)
                elif hasattr(instance, "post"):
                    return instance.post(request, *args, **kwargs)
            raise Http404()
        raise Http404()

    def ajax_get(self, request, *args, **kwargs):
        if "instance_id" in kwargs:
            plugin, instance = self.plugin_instance(kwargs["instance_id"])
            if hasattr(plugin, "ajax_get"):  # and request.is_ajax():
                request.GET = QueryDict(request.body)
                try:
                    params = (
                        self.decode_path(kwargs["parameter"])
                        if "parameter" in kwargs
                        else {}
                    )
                    return plugin.ajax_get(request, instance, params)
                except ValidationError as error:
                    return JsonResponse({"result": "error", "msg": str(error.args[0])})
        elif "form_id" in kwargs:
            if kwargs["form_id"] in _formview_pool:
                form_id = kwargs.pop("form_id")
                instance = _formview_pool[form_id][0](**kwargs)
                if hasattr(instance, "ajax_get"):
                    return instance.ajax_get(request, *args, **kwargs)
                elif hasattr(instance, "get"):
                    return instance.get(request, *args, **kwargs)
            raise Http404()
        raise Http404()
