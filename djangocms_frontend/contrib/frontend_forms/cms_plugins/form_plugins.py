from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.contrib.frontend_forms import forms, models
from djangocms_frontend.helpers import add_plugin, delete_plugin, insert_fields

from .. import forms as forms_module
from .ajax_plugins import FormPlugin

mixin_factory = settings.get_renderer(forms_module)


class FormElementPlugin(CMSUIPlugin):
    top_element = FormPlugin.__name__
    module = _("Forms")
    render_template = f"djangocms_frontend/{settings.framework}/widgets/base.html"
    settings_name = _("Settings")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("field_name", "field_label"),
                    ("field_required", "field_placeholder"),
                )
            },
        ),
    )

    @classmethod
    def get_parent_classes(cls, slot, page, instance=None):
        """Only valid as indirect child of the cls.top_element"""
        if instance is None:
            return [""]
        parent = instance
        while parent is not None:
            if parent.plugin_type == cls.top_element:
                return super().get_parent_classes(slot, page, instance)
            parent = parent.parent
        return [""]

    def get_fieldsets(self, request, obj=None):
        if hasattr(self, "settings_fields"):
            return insert_fields(
                super().get_fieldsets(request, obj),
                self.settings_fields,
                block=None,
                position=-1,
                blockname=self.settings_name,
                blockattrs=dict(classes=()),
            )
        return super().get_fieldsets(request, obj)

    def render(self, context, instance, placeholder):
        instance.add_classes("form-control")
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CharFieldPlugin(mixin_factory("CharField"), FormElementPlugin):
    name = _("Text")
    model = models.CharField
    form = forms.CharFieldForm
    settings_fields = (("min_length", "max_length"),)


@plugin_pool.register_plugin
class EmailFieldPlugin(mixin_factory("EmailField"), FormElementPlugin):
    name = _("Email")
    model = models.EmailField
    form = forms.EmailFieldForm


@plugin_pool.register_plugin
class URLFieldPlugin(mixin_factory("URLField"), FormElementPlugin):
    name = _("URL")
    model = models.UrlField
    form = forms.UrlFieldForm


@plugin_pool.register_plugin
class DecimalFieldPlugin(mixin_factory("DecimalField"), FormElementPlugin):
    name = _("Decimal")
    model = models.DecimalField
    form = forms.DecimalFieldForm
    settings_fields = ("decimal_places", ("min_value", "max_value"))


@plugin_pool.register_plugin
class IntegerFieldPlugin(mixin_factory("IntegerField"), FormElementPlugin):
    name = _("Integer")
    model = models.IntegerField
    form = forms.IntegerFieldForm
    settings_fields = (("min_value", "max_value"),)


@plugin_pool.register_plugin
class TextareaPlugin(FormElementPlugin):
    name = _("Textarea")
    model = models.TextareaField
    form = forms.TextareaFieldForm
    settings_fields = (
        "field_rows",
        ("min_length", "max_length"),
    )


@plugin_pool.register_plugin
class DateFieldPlugin(FormElementPlugin):
    name = _("Date")
    model = models.DateField
    form = forms.DateFieldForm


@plugin_pool.register_plugin
class DateTimeFieldPlugin(FormElementPlugin):
    name = _("Date and time")
    model = models.DateTimeField
    form = forms.DateTimeFieldForm


@plugin_pool.register_plugin
class TimeFieldPlugin(FormElementPlugin):
    name = _("Time")
    model = models.TimeField
    form = forms.TimeFieldForm


@plugin_pool.register_plugin
class SelectPlugin(mixin_factory("SelectField"), FormElementPlugin):
    name = _("Select")

    model = models.Select
    form = forms.SelectFieldForm
    allow_children = True
    child_classes = ["ChoicePlugin"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("field_name", "field_label"),
                    "field_select",
                    "field_required",
                )
            },
        ),
        (
            _("Choices"),
            {
                "classes": ("collapse",),
                "description": _(
                    "Use this field to quick edit choices. Choices can be added (<kbd>+</kbd>), deleted "
                    "(<kbd>&times;</kbd>) and updated. On the left side enter the value to be stored in the database. "
                    "On the right side enter the text to be shown to the user. The order of choices can be adjusted "
                    "in the structure tree <b>after saving</b> the edits."
                ),
                "fields": ("field_choices",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Reflects the quick edit changes in the plugin tree"""
        super().save_model(request, obj, form, change)
        child_plugins = obj.get_children()
        children = {}
        for child in child_plugins:
            child_ui = child.djangocms_frontend_frontenduiitem
            children[child_ui.config["value"]] = child_ui
        position = len(child_plugins)
        data = form.cleaned_data
        for value, verbose in data["field_choices"]:
            child = children.pop(value, None)
            if child is not None:  # Need to update?
                if verbose != child.config["verbose"]:
                    child.config["verbose"] = verbose
                    child.save()
            else:  # Not in there, add it!
                add_plugin(
                    obj.placeholder,
                    models.Choice(
                        parent=obj,
                        placeholder=obj.placeholder,
                        position=obj.position + position + 1,
                        language=obj.language,
                        plugin_type=ChoicePlugin.__name__,
                        ui_item=models.Choice.__class__.__name__,
                        config=dict(value=value, verbose=verbose),
                    ),
                )
                position += 1
        for _key, child in children.items():  # Delete remaining
            delete_plugin(child)


@plugin_pool.register_plugin
class ChoicePlugin(mixin_factory("ChoiceField"), CMSUIPlugin):
    name = _("Choice")
    module = _("Forms")
    fieldsets = ((None, {"fields": (("value", "verbose"),)}),)
    model = models.Choice
    form = forms.ChoiceForm
    require_parent = True
    parent_classes = ["SelectPlugin"]


@plugin_pool.register_plugin
class BooleanFieldPlugin(mixin_factory("BooleanField"), FormElementPlugin):
    name = _("Boolean")
    model = models.BooleanField
    form = forms.BooleanFieldForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("field_name", "field_label"),
                    "field_as_switch",
                    "field_required",
                )
            },
        ),
    )
