from cms.models import CMSPlugin
from cms.utils.compat import DJANGO_3_0
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext

from djangocms_frontend.fields import TagTypeField
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO

if DJANGO_3_0:
    from django_jsonfield_backport.models import JSONField
else:
    JSONField = models.JSONField


class FrontendUIItem(CMSPlugin):
    """
    Generic plugin model to store all frontend items. Plugin-specific information is stored in a JSON field
    called "config".
    """

    class Meta:
        verbose_name = gettext("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField(blank=True)
    config = JSONField(default=dict, encoder=DjangoJSONEncoder)

    def __init__(self, *args, **kwargs):
        self._additional_classes = []
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        """Makes properties of plugin config available as plugin properties."""
        if (
            item[0] != "_" and item in self.config
        ):  # Avoid infinite recursion trying to get .config from db
            return self.config[item]
        return super().__getattribute__(item)

    def __str__(self):
        if "__str__" in self.config:
            return self.config["__str__"]
        return f"{gettext(self.ui_item)} ({str(self.pk)})"

    def add_classes(self, *args):
        for arg in args:
            if arg:
                self._additional_classes += arg.split() if isinstance(arg, str) else arg

    def add_attribute(self, attr, value=None):
        attrs = self.config.get("attributes", {})
        if attr == "style" and attr in attrs:
            value += attrs[attr]
        attrs.update({attr: value})
        self.config["attributes"] = attrs

    def get_attributes(self):
        attributes = self.config.get("attributes", {})
        classes = set(attributes.get("class", "").split())
        classes.update(self._additional_classes)
        if classes:
            attributes["class"] = " ".join(classes)
        parts = (
            f'{item}="{conditional_escape(value)}"' if value else f"{item}"
            for item, value in attributes.items()
        )
        attributes_string = " ".join(parts)
        return mark_safe(" " + attributes_string) if attributes_string else ""

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def initialize_from_form(self, form=None):
        """Populates the config JSON field based on initial values provided by the fields of form"""
        if form is None:
            form = self.get_plugin_class().form
        if isinstance(form, type):  # if is class
            form = form()  # instantiate
        entangled_fields = getattr(
            getattr(form, "Meta", None), "entangled_fields", {}
        ).get("config", ())
        for field in entangled_fields:
            self.config.setdefault(
                field, {} if field == "attributes" else form[field].initial or ""
            )
        return self

    def get_short_description(self):
        """Plugin-specific short description (to be defined by subclasses)"""
        return ""

    @property
    def framework_info(self):
        return FRAMEWORK_PLUGIN_INFO.get(self.__class__.__name__, None)
