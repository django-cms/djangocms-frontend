from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext

from djangocms_frontend.fields import AttributesField, TagTypeField


class FrontendUIItem(CMSPlugin):
    """
    Generic plugin model to store all frontend items
    """

    class Meta:
        verbose_name = gettext("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField(blank=True)
    config = models.JSONField(default=dict)

    default_config = {}

    def __getattr__(self, item):
        if (
            item[0] != "_" and item in self.config
        ):  # Avoid infinite recursion trying to get .config from db
            return self.config[item]
        if item in self.default_config:
            return self.default_config[item]
        return super().__getattribute__(item)

    def __str__(self):
        if "__str__" in self.config:
            return self.config["__str__"]
        return f"{gettext(self.ui_item)} ({str(self.pk)})"

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def initialize_from_form(self, form):
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
        pass
