from django.core.exceptions import ImproperlyConfigured

try:
    import filer
except ImportError:
    raise ImproperlyConfigured(
        "Image fields require django-filer. "
        "Install it using: pip install djangocms-frontend[filer]"
    )

from django.db.models import ManyToOneRel
from filer.fields.image import AdminImageFormField, FilerImageField
from filer.models import Image


class ImageFormField(AdminImageFormField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("rel", ManyToOneRel(FilerImageField, Image, "id"))
        kwargs.setdefault("queryset", Image.objects.all())
        kwargs.setdefault("to_field_name", "id")
        super().__init__(*args, **kwargs)
