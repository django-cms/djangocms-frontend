import copy
import decimal

from cms.constants import SLUG_REGEXP
from cms.plugin_base import CMSPluginBase
from cms.utils.conf import get_cms_setting
from django.apps import apps
from django.contrib.admin.helpers import AdminForm
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template
from django.urls import re_path
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO


def get_related_object(scope, field_name):
    """
    Returns the related field, referenced by the content of a ModelChoiceField.
    """
    try:
        Model = apps.get_model(scope[field_name]["model"])
        relobj = Model.objects.get(pk=scope[field_name]["pk"])
    except (ObjectDoesNotExist, LookupError, TypeError):
        relobj = None
    return relobj


class get_related:
    """Descriptor lazily getting related objects from the config dict."""

    def __init__(self, key):
        self.key = key

    def __get__(self, instance, owner):
        obj = get_related_object(instance.config, self.key)
        if obj is not None:
            setattr(instance, self.key, obj)
        return obj


def insert_fields(fieldsets, new_fields, block=None, position=-1, blockname=None, blockattrs=None):
    """
    creates a copy of fieldsets inserting the new fields either in the indexed block at the position,
    or - if no block is given - at the end
    """
    if blockattrs is None:
        blockattrs = dict()
    if block is None:
        fs = (
            list(fieldsets[:position] if position != -1 else fieldsets)
            + [
                (
                    blockname,
                    {
                        "classes": ("collapse",) if len(fieldsets) > 0 else (),
                        "fields": list(new_fields),
                        **blockattrs,
                    },
                )
            ]
            + list(fieldsets[position:] if position != -1 else [])
        )
        return fs
    modify = copy.deepcopy(fieldsets[block])
    fields = modify[1]["fields"]
    if position >= 0:
        modify[1]["fields"] = list(fields[:position]) + list(new_fields) + list(fields[position:])
    else:
        modify[1]["fields"] = (
            list(fields[: position + 1] if position != -1 else fields)
            + list(new_fields)
            + list(fields[position + 1 :] if position != -1 else [])
        )
    fs = (
        list(fieldsets[:block] if block != -1 else fieldsets)
        + [modify]
        + list(fieldsets[block + 1 :] if block != -1 else [])
    )
    return fs


def first_choice(choices):
    for value, verbose in choices:
        if not isinstance(verbose, (tuple, list)):
            return value
        else:
            first = first_choice(verbose)
            if first is not None:
                return first
    return None


def get_template_path(prefix, template, name):
    return f"djangocms_frontend/{settings.framework}/{prefix}/{template}/{name}.html"


def get_plugin_template(instance, prefix, name, templates):
    template = getattr(instance, "template", first_choice(templates))
    template_path = get_template_path(prefix, template, name)

    try:
        select_template([template_path])
    except TemplateDoesNotExist:
        # TODO render a warning inside the template
        template_path = get_template_path(prefix, "default", name)

    return template_path


# use mark_safe_lazy to delay the translation when using mark_safe
# otherwise they will not be added to /locale/
# https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#other-uses-of-lazy-in-delayed-translations
mark_safe_lazy = lazy(mark_safe, str)


def link_to_framework_doc(ui_item, topic):
    link = FRAMEWORK_PLUGIN_INFO.get(ui_item, {}).get(topic, None)
    if link:
        return mark_safe_lazy(
            _('Read more in the <a href="{link}" target="_blank">documentation</a>.').format(link=link)
        )
    return None


def add_plugin(placeholder, plugin):
    """CMS version-save function to add a plugin to a placeholder"""
    if hasattr(placeholder, "add_plugin"):  # available as of CMS v4
        placeholder.add_plugin(plugin)
    else:  # CMS < v4
        if plugin.parent:
            plugin.position -= plugin.parent.position + 1  # Restart position counting at 0
        else:
            plugin.position -= 1  # 0-based counting in v3
        plugin.save()


def delete_plugin(plugin):
    """CMS version save function to delete a plugin (and its descendants) from a placeholder"""
    return plugin.placeholder.delete_plugin(plugin)


def is_first_child(instance, parent):
    if hasattr(instance.placeholder, "add_plugin"):  # available as of CMS v4
        return instance.position == parent.position + 1
    else:
        return instance.position == 0


def coerce_decimal(value):
    """Force value to be converted to decimal.Decimal or return None"""
    try:
        return decimal.Decimal(value)
    except TypeError:
        return None


class FrontendEditableAdminMixin:
    """
    Adding ``FrontendEditableAdminMixin`` to  models admin class allows to open that admin
    in the frontend by double-clicking on fields rendered with the ``render_model`` template
    tag.
    """

    frontend_editable_fields = []

    def get_urls(self):  # pragma: no cover
        """
        Register the url for the single field edit view
        """
        info = f"{self.model._meta.app_label}_{self.model._meta.model_name}"

        def pat(regex, fn):
            return re_path(regex, self.admin_site.admin_view(fn), name=f"{info}_{fn.__name__}")

        url_patterns = [
            pat(r"edit-field/(%s)/([a-z\-]+)/$" % SLUG_REGEXP, self.edit_field),
        ]
        return url_patterns + super().get_urls()

    def _get_object_for_single_field(self, object_id, language):  # pragma: no cover
        # Quick and dirty way to retrieve objects for django-hvad
        # Cleaner implementation will extend this method in a child mixin
        try:
            # First see if the model uses the admin manager pattern from cms.models.manager.ContentAdminManager
            manager = self.model.admin_manager
        except AttributeError:
            # If not, use the default manager
            manager = self.model.objects
        try:
            return manager.language(language).get(pk=object_id)
        except AttributeError:
            return manager.get(pk=object_id)

    def edit_field(self, request, object_id, language):
        obj = self._get_object_for_single_field(object_id, language)
        opts = obj.__class__._meta
        saved_successfully = False
        cancel_clicked = request.POST.get("_cancel", False)
        raw_fields = request.GET.get("edit_fields")
        fields = [field for field in raw_fields.split(",") if field in self.frontend_editable_fields]
        if not fields:
            context = {"opts": opts, "message": _("Field %s not found") % raw_fields}
            return render(request, "admin/cms/page/plugin/error_form.html", context)
        if not request.user.has_perm(f"{self.model._meta.app_label}.change_{self.model._meta.model_name}"):
            context = {"opts": opts, "message": _("You do not have permission to edit this item")}
            return render(request, "admin/cms/page/plugin/error_form.html", context)
            # Dynamically creates the form class with only `field_name` field
        # enabled
        form_class = self.get_form(request, obj, fields=fields)
        if not cancel_clicked and request.method == "POST":
            form = form_class(instance=obj, data=request.POST)
            if form.is_valid():
                new_object = form.save(commit=False)
                self.save_model(request, new_object, form, change=True)
                saved_successfully = True
        else:
            form = form_class(instance=obj)
        admin_form = AdminForm(form, fieldsets=[(None, {"fields": fields})], prepopulated_fields={}, model_admin=self)
        media = self.media + admin_form.media
        context = {
            "CMS_MEDIA_URL": get_cms_setting("MEDIA_URL"),
            "title": opts.verbose_name,
            "plugin": None,
            "plugin_id": None,
            "adminform": admin_form,
            "add": False,
            "is_popup": True,
            "media": media,
            "opts": opts,
            "change": True,
            "save_as": False,
            "has_add_permission": False,
            "window_close_timeout": 10,
        }
        if cancel_clicked:
            # cancel button was clicked
            context.update(
                {
                    "cancel": True,
                }
            )
            return render(request, "admin/cms/page/plugin/confirm_form.html", context)
        if not cancel_clicked and request.method == "POST" and saved_successfully:
            if isinstance(self, CMSPluginBase):
                if hasattr(obj.placeholder, "mark_as_dirty"):
                    # Only relevant for v3: mark the placeholder as dirty so user can publish changes
                    obj.placeholder.mark_as_dirty(obj.language, clear_cache=False)
                # Update the structure board by populating the data bridge
                return self.render_close_frame(request, obj)
            return render(request, "admin/cms/page/plugin/confirm_form.html", context)
        return render(request, "admin/cms/page/plugin/change_form.html", context)
