from django.core.files.base import ContentFile

from djangocms_frontend.contrib.image.cms_plugins import ImagePlugin
from djangocms_frontend.contrib.image.forms import get_templates
from djangocms_frontend.contrib.image.models import Image
from djangocms_frontend.helpers import add_plugin, first_choice

default_template = first_choice(get_templates())


def create_image_plugin(filename, file, parent_plugin, **kwargs):
    # Set the FilerImageField value.
    from filer.settings import FILER_IMAGE_MODEL
    from filer.utils.loader import load_model

    image_class = load_model(FILER_IMAGE_MODEL)
    image_obj = image_class(file=ContentFile(file.read(), name=filename))
    image_obj.save()

    img = Image(
        parent=parent_plugin,
        position=parent_plugin.position + 1,
        placeholder=parent_plugin.placeholder,
        language=parent_plugin.language,
        plugin_type=ImagePlugin.__name__,
        ui_item=Image.__class__.__name__,
        config={},
    ).initialize_from_form()
    img.config.update(
        {
            "picture": {"pk": image_obj.pk, "model": "filer.image"},
            "use_no_cropping": True,
        }
    )
    add_plugin(parent_plugin.placeholder, img)

    return img
