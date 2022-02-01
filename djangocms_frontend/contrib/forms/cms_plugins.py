from urllib.parse import urlencode

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.http import Http404, JsonResponse
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormMixin
from sekizai.context import SekizaiContext

from djangocms_frontend import settings
from djangocms_frontend.contrib import forms as forms_module

from . import forms, models


class CMSAjaxBase(CMSPluginBase):
    def ajax_post(self, request, instance, parameter):
        return JsonResponse({})

    def ajax_get(self, request, instance, parameter):
        return JsonResponse({})


class AjaxFormMixin(FormMixin):
    form_class = None
    replace = True
    request = None
    instance = None
    parameter = {}
    template_name = None

    def json_return(self, errors, result, redirect, content):
        return JsonResponse(
            {
                "result": result,
                "redirect": redirect,
                "errors": errors,
                "field_errors": {},
                "content": content,
            }
        )

    def form_valid(self, form):
        save = getattr(form, "save", None)
        redirect = getattr(form, "redirect", None)
        try:
            redirect = reverse(redirect)
        except NoReverseMatch:
            pass

        if callable(save):
            form.save()
        get_success_context = "get_success_context"
        render_success = "render_success"
        if hasattr(form, "slug"):
            get_success_context += "_" + form.slug
            render_success += "_" + form.slug

        if hasattr(form, render_success):
            context = SekizaiContext(
                {
                    "form": form,
                    "instance": self.instance,
                    "request": self.request,
                    "get_str": urlencode(
                        {x: y for x, y in self.request.POST.items() if "csrf" not in x}
                    ),
                }
            )
            if hasattr(form, get_success_context):
                get_success_context = getattr(form, get_success_context)
                context.update(get_success_context(self.request, self.instance, form))
            errors, result, redir, content = (
                [],
                context.get("result", "success"),
                "" if self.replace else "result",
                render_to_string(
                    getattr(form, render_success), context.flatten(), self.request
                ),
            )
        elif redirect:
            errors, result, redir, content = (
                [],
                "success",
                redirect,
                "",
            )
        else:
            errors, result, redir, content = (
                [_("No content in response from")],
                "error",
                "",
                "",
            )
        redirect = redirect or redir
        return JsonResponse(
            {
                "result": result,
                "redirect": redirect,
                "errors": errors,
                "field_errors": {},
                "content": content,
            }
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "result": "invalid form",
                "errors": form.non_field_errors(),
                "field_errors": {
                    key + str(self.instance.id): value
                    for key, value in form.errors.items()
                },
                "html": form.render(context=csrf(self.request))
                if hasattr(form, "render")
                else "",  # Kills reCAPTCHA
            }
        )

    def get_form_class(self, slug=None):
        if hasattr(self, "form_classes") and isinstance(self.form_classes, list):
            slug = slug or getattr(self, "parameter", {}).get("s", "")
            if not slug:
                return self.form_classes[0]
            for cls in self.form_classes:
                if getattr(cls, "slug", None) == slug:
                    return cls
            raise Http404
        return super().get_form_class()

    def get_initial(self, slug=None):
        slug = slug or getattr(self, "parameter", {}).get("s", "")
        initial = "initial_" + slug
        if hasattr(self, initial):
            return getattr(self, initial)
        return super().get_initial()

    def get_form_kwargs(self, slug=None):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(slug),
            "prefix": self.get_prefix(),
            "label_suffix": "",
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_ajax_form(self, slug=None):
        form_class = self.get_form_class(slug)
        if form_class:
            form = form_class(**self.get_form_kwargs(slug))
            if self.instance:
                for field in form.base_fields:
                    form.fields[field].widget.attrs.update(
                        {"id": field + str(self.instance.id)}
                    )
            return form
        return None

    def ajax_post(self, request, instance, parameter=None):
        if parameter is None:
            parameter = {}
        self.request = request
        self.instance = instance
        self.parameter = parameter

        form = self.get_ajax_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def ajax_get(self, request, instance, parameter=None):
        if parameter is None:
            parameter = {}
        self.request = request
        self.instance = instance
        self.parameter = parameter
        context = self.get_context_data(**parameter)
        errors, redirect, content = (
            [],
            "",
            render_to_string(self.template_name, context.flatten(), self.request),
        )
        return JsonResponse(
            {
                "result": (
                    ("result" if redirect == "result" else "success")
                    if errors == []
                    else "error"
                ),
                "redirect": redirect,
                "errors": errors,
                "field_errors": {},
                "content": content,
            }
        )


class CMSAjaxForm(AjaxFormMixin, CMSAjaxBase):
    def get_form(self, request, *args, **kwargs):
        """
        get_form needs to come from CMSAjaxBase and NOT from AjaxFormMixin
        for admin to work
        """
        return super(CMSAjaxBase, self).get_form(request, *args, **kwargs)

    def set_context(self, context, instance, placeholder):
        return {}

    def render(self, context, instance, placeholder):
        self.instance = instance
        self.request = context["request"]

        form = self.get_ajax_form()
        context.update(self.set_context(context, instance, placeholder))
        context.update({"instance": instance, "form": form})
        return context


mixin_factory = settings.get_renderer(forms_module)


@plugin_pool.register_plugin
class FormPlugin(mixin_factory("Forms"), CMSAjaxForm):
    """
    Components > "Alerts" Plugin
    https://getbootstrap.com/docs/5.0/components/alerts/
    """

    name = _("Form")
    module = _("Frontend")
    model = models.Form

    form = forms.FormsForm
    render_template = f"djangocms_frontend/{settings.framework}/form.html"
    change_form_template = "djangocms_frontend/admin/forms.html"
    allow_children = False

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "form_selection",
                ],
            },
        ),
        (
            _("Submit button"),
            {
                "classes": ("collapse",),
                "fields": [
                    ("form_submit_message", "form_submit_align"),
                    "form_submit_context",
                ],
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def get_form_class(self, slug=None):
        if self.instance.config.get("form_selection", None):
            return forms._form_registry.get(self.instance.form_selection, None)
        return None
