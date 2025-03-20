from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin

from djangocms_frontend.fields import AttributesFormField
from djangocms_frontend.helpers import insert_fields


class AttributesMixin:
    block_attr = {
        "description": _(
            "Advanced settings lets you add html attributes to render this element. Use them wisely and rarely."
        ),
        "classes": (
            "collapse",
            "attributes",
        ),
    }

    def get_fieldsets(self, request, obj=None):
        meta = self.form._meta
        fields = ["tag_type"] if "tag_type" in getattr(meta, "untangled_fields", ()) else []
        fields.append("attributes")
        return insert_fields(
            super().get_fieldsets(request, obj),
            fields,
            blockname=_("Advanced settings"),
            blockattrs=self.block_attr,
            position=-1,  # Always last
        )


class AttributesFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            "config": [
                "attributes",
            ]
        }

    attributes = AttributesFormField()
