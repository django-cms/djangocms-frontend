from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext

from djangocms_frontend.fields import AttributesField, TagTypeField

from .settings import prepare_instance


class FrontendUIItem(CMSPlugin):
    """
    Generic plugin model to store all frontend items
    """

    class Meta:
        verbose_name = gettext("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField()
    config = models.JSONField()
    attributes = AttributesField()

    def __getattr__(self, item):
        if (
            item[0] != "_" and item in self.config
        ):  # Avoid infinite recursion trying to get .config from db
            return self.config[item]
        return super().__getattribute__(item)

    def __str__(self):
        return f"{gettext(self.ui_item)} ({str(self.pk)})"

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        prepare_instance(self)
        return super().save(*args, **kwargs)

    def get_short_description(self):
        pass
