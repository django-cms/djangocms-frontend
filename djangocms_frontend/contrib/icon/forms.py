from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField, TagTypeFormField
from .fields import IconPickerField

from ...common.responsive import ResponsiveFormMixin
from ...models import FrontendUIItem


class IconForm(ResponsiveFormMixin, EntangledModelForm):
    """
    Layout > "Media" Plugin
    http://getbootstrap.com/docs/4.0/layout/media-object/
    """

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "icon",
                "attributes",
            ]
        }
        untangled_fields = ("tag_type",)

    icon = IconPickerField()
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

