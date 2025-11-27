from cms.models import CMSPlugin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.fields import TagTypeField
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO


class AbstractFrontendUIItem(CMSPlugin):
    """
    The `AbstractFrontendUIItem` class is an abstract base class that provides common functionality
    for frontend UI items in a CMS plugin. It is a subclass of `CMSPlugin` class.

    Use this class as a base class for custom plugins that add their own database fields.

    Attributes:
        - ui_item: A CharField that represents the UI item name (max length 30).
        - tag_type: A TagTypeField (custom field) that represents the type of HTML tag for the UI item.
        - config: A JSONField that stores additional configuration for the UI item.

    Methods:
        - __init__(*args, **kwargs): Constructor method that initializes the object and sets additional classes.
        - __getattr__(item): Allows properties of the plugin config to be accessed as plugin properties.
        - __str__(): Returns a string representation of the UI item.
        - add_classes(*args): Adds additional classes to the UI item.
        - add_attribute(attr, value=None): Adds an attribute to the configuration attributes.
        - get_attributes(): Returns the attributes as a string for rendering the UI item.
        - save(*args, **kwargs): Saves the UI item to the database.
        - initialize_from_form(form=None): Populates the config JSON field based on initial values from a form.
        - get_short_description(): Returns a plugin-specific short description.
        - framework_info: Returns the framework information for the UI item.

    Note: This is an abstract base class and should not be used directly.
    """

    class Meta:
        abstract = True
        verbose_name = _("UI item")

    ui_item = models.CharField(max_length=30)
    tag_type = TagTypeField(blank=True)
    config = models.JSONField(default=dict, encoder=DjangoJSONEncoder)

    def __init__(self, *args, **kwargs):
        self._additional_classes = []
        self.html_id = None  # HTML id attribute will be set in template tag set_html_id.
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        """Makes properties of plugin config available as plugin properties."""
        if item[0] != "_" and item in self.config:  # Avoid infinite recursion trying to get .config from db
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

    def add_attribute(self, attr, value=None):
        attrs = self.config.get("attributes", {})
        if attr == "style" and attr in attrs:
            value += attrs[attr]
        attrs.update({attr: value})
        self.config["attributes"] = attrs

    def get_attributes(self):
        attributes = self.config.get("attributes", {})
        classes = self.get_classes()  # get classes
        classes = (f'class="{classes}"') if classes else ""  # to string
        parts = (
            f'{item}="{conditional_escape(value)}"' if value else f"{item}"
            for item, value in attributes.items()
            if item != "class"
        )
        attributes_string = (classes + " ".join(parts)).strip()
        return mark_safe(" " + attributes_string) if attributes_string else ""

    def get_classes(self):
        attributes = self.config.get("attributes", {})
        classes = set(attributes.get("class", "").split())  # classes added in attriutes
        classes.update(self._additional_classes)  # add additional classes
        return conditional_escape(" ".join(classes))

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def initialize_from_form(self, form=None):
        """Populates the config JSON field based on initial values provided by the fields of form"""
        if form is None:
            form = self.get_plugin_class().form
        if isinstance(form, type):  # if is class
            if not getattr(form._meta, "model", None):
                form._meta.model = self.__class__
            form = form()  # instantiate
        entangled_fields = getattr(getattr(form, "_meta", None), "entangled_fields", {}).get("config", ())
        for field in entangled_fields:
            self.config.setdefault(field, {} if field == "attributes" else form[field].initial or "")
        return self

    def get_short_description(self):
        """Plugin-specific short description (to be defined by subclasses). Try title attribute first."""
        return self.config.get("title", "")

    @property
    def framework_info(self):
        return FRAMEWORK_PLUGIN_INFO.get(self.__class__.__name__, None)


class FrontendUIItem(AbstractFrontendUIItem):
    """

    Class: FrontendUIItem

    Inherits From: AbstractFrontendUIItem

    Description:
    This class represents a UI item in the frontend. It is used to define the behavior and attributes
    of a UI item in the user interface.

    Use this class as a base class for custom plugins that do not add their own database fields but
    use the entangled form fields instead.

    Attributes:
    - verbose_name (str): The verbose name of the UI item.

    Methods:
    None

    """

    class Meta:
        verbose_name = _("UI item")
