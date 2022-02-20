from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend import settings
from djangocms_frontend.fields import ButtonGroup
from djangocms_frontend.helpers import insert_fields


class JumbotronRenderMixin:
    def render(self, context, instance, placeholder):
        if not getattr(instance, "background_context", False):
            instance.add_classes("bg-light")
        return super().render(context, instance, placeholder)
