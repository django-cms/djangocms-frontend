from entangled.forms import EntangledModelForm

from djangocms_frontend.fields import AttributesFormField

from ...models import FrontendUIItem


class MediaForm(EntangledModelForm):
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
