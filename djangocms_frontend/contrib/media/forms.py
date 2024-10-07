from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField, TagTypeFormField

from ...common import ResponsiveFormMixin
from ...models import FrontendUIItem


class MediaForm(ResponsiveFormMixin, EntangledModelForm):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    attributes = AttributesFormField()
    tag_type = TagTypeFormField()


class MediaBodyForm(EntangledModelForm):
    """
    Layout > "Media body" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
