from urllib.parse import urlencode

from cms.plugin_pool import plugin_pool
from django.http import Http404, JsonResponse
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormMixin
from sekizai.context import SekizaiContext

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.contrib import frontend_forms as forms_module
from djangocms_frontend.contrib.frontend_forms import forms, models, recaptcha
from djangocms_frontend.contrib.frontend_forms.forms import SimpleFrontendForm
from djangocms_frontend.contrib.frontend_forms.helper import get_option
from djangocms_frontend.helpers import insert_fields, mark_safe_lazy


class CMSAjaxBase(CMSUIPlugin):
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
        redirect = get_option(form, "redirect", None)
        if isinstance(redirect, str):
            try:
                redirect = reverse(redirect)
            except NoReverseMatch:
                pass
        elif hasattr(redirect, "get_absolute_url"):
            redirect = redirect.get_absolute_url()

        if callable(save):
            form.save()
        get_success_context = "get_success_context"
        render_success = "render_success"
        if hasattr(form, "slug"):
            get_success_context += "_" + form.slug
            render_success += "_" + form.slug

        if get_option(form, render_success, None):
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
                    get_option(form, render_success), context.flatten(), self.request
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
            return getattr(self, initial).copy()
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
            if getattr(form_class, "takes_request", False):
                form = form_class(request=self.request, **self.get_form_kwargs(slug))
            else:
                form = form_class(**self.get_form_kwargs(slug))
            if self.instance:
                for field in form.base_fields:
                    form.fields[field].widget.attrs.update(
                        {"id": (field or "") + str(self.instance.id)}
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
class FormPlugin(mixin_factory("Form"), AttributesMixin, CMSAjaxForm):
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
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "form_selection",
                    "form_name",
                    (
                        "form_login_required",
                        "form_unique",
                    ),
                    "form_floating_labels",
                    "form_spacing",
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
            _("Actions"),
            {
                "classes": ("collapse",),
                "fields": ["form_actions"],
            },
        ),
    ]

    def get_fieldsets(self, request, obj=None):
        if recaptcha.installed:
            return insert_fields(
                super().get_fieldsets(request, obj),
                ("captcha_widget", "captcha_requirement", "captcha_config"),
                block=None,
                position=1,
                blockname=_("reCaptcha"),
                blockattrs={}
                if recaptcha.keys_available
                else dict(
                    description=mark_safe_lazy(
                        _(
                            '<blockquote style="color: var(--error-fg);">Please get a public and secret '
                            'key from <a href="{key_link}" target="_blank">Google</a> '
                            "and ensure that they are available through django settings "
                            "<code>RECAPTCHA_PUBLIC_KEY</code> and <code>RECAPTCHA_PRIVATE_KEY</code>. "
                            "Without these keys captcha protection will not work.</blockquote>"
                        ).format(key_link="https://developers.google.com/recaptcha")
                    )
                ),
            )
        return super().get_fieldsets(request, obj)

    def get_form_class(self, slug=None):
        if self.instance.child_plugin_instances is None:  # not set if in ajax_post
            self.instance.child_plugin_instances = [
                child.get_plugin_instance()[0] for child in self.instance.get_children()
            ]
        if self.instance.child_plugin_instances:
            return self.create_form_class_from_plugins()
        if self.instance.config.get("form_selection", None):
            return forms._form_registry.get(self.instance.form_selection, None)
        return None

    def create_form_class_from_plugins(self):
        def traverse(instance):
            """Recursively traverse children to identify form fields (by them having a method called
            "get_form_field" """
            nonlocal fields
            if hasattr(instance, "get_form_field"):
                name, field = instance.get_form_field()
                fields[name] = field
            if (
                instance.child_plugin_instances is None
            ):  # children already fetched from db?
                instance.child_plugin_instances = [
                    child.get_plugin_instance()[0] for child in instance.get_children()
                ]
            for child in instance.child_plugin_instances:
                traverse(child)

        fields = {}
        traverse(self.instance)

        # Add recaptcha field in necessary
        if recaptcha.installed and self.instance.config.get("captcha_widget"):
            fields[recaptcha.field_name] = recaptcha.get_recaptcha_field(
                self.instance.config
            )

        # Collect meta options for Meta class
        meta_options = dict(form_name=self.instance.config.get("form_name", "unset"))
        if self.instance.config.get("form_floating_labels", False):
            meta_options["floating_labels"] = True
        meta_options[
            "field_sep"
        ] = f'mb-{self.instance.config.get("form_spacing", "3")}'  # TODO: This is bootstrap-specific
        meta_options[
            "redirect"
        ] = self.instance.placeholder.page  # Default behavior: redirect to same page
        meta_options["login_required"] = self.instance.config.get(
            "form_login_required", False
        )
        meta_options["unique"] = self.instance.config.get("form_unique", False)
        meta_options["form_actions"] = self.instance.config.get("form_actions", [])
        fields["Meta"] = type("Meta", (), dict(options=meta_options))  # Meta class

        return type(
            "FrontendAutoForm",
            (SimpleFrontendForm,),
            fields,
        )

    @classmethod
    def get_parent_classes(cls, slot, page, instance=None):
        """Avoid form in a form"""
        if instance is None or instance.parent is None:
            return super().get_parent_classes(slot, page, instance)
        parent = instance.parent
        while parent is not None:
            if parent.plugin_type == cls.__name__:
                return [""]
            parent = parent.parent
        return super().get_parent_classes(slot, page, instance)

    def render(self, context, instance, placeholder):
        self.instance = instance
        instance.add_classes("djangocms-frontend-ajax-form")
        context["RECAPTCHA_PUBLIC_KEY"] = recaptcha.RECAPTCHA_PUBLIC_KEY
        return super().render(context, instance, placeholder)
