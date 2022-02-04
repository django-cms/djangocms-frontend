from cms.models import CMSPlugin
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext

from djangocms_frontend.fields import TagTypeField
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO


class FrontendUIItem(CMSPlugin):
    """
    Generic plugin model to store all frontend items. Plugin-specific information is stored in a JSON field
    called "config".
    """

    class Meta:
        verbose_name = gettext("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField(blank=True)
    config = models.JSONField(default=dict)

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

    def get_attributes(self):
        classes = (
            set(self.config["attributes"].get("class", "").split())
            if "attributes" in self.config
            else set()
        )
        classes.update(self._additional_classes)
        parts = (
            f'{item}="{conditional_escape(value)}"' if value else f"{item}"
            for item, value in {
                **self.config.get("attributes", {}),
                **{"class": " ".join(classes)},
            }.items()
        )
        return mark_safe(" " + " ".join(parts))

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def initialize_from_form(self, form):
        """Populates the config JSON field based on initial values provided by the fields of form"""
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
        pass

    @property
    def framework_info(self):
        return FRAMEWORK_PLUGIN_INFO.get(self.ui_item, None)
