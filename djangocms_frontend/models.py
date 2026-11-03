import copy

from cms.models import CMSPlugin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.fields import TagTypeField
from djangocms_frontend.settings import FRAMEWORK_PLUGIN_INFO, PLUGIN_DEFAULTS, SHOW_ADVANCED_SETTINGS


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
        self.html_id: str | None = None  # HTML id attribute will be set in template tag set_html_id.
        super().__init__(*args, **kwargs)
        if not SHOW_ADVANCED_SETTINGS:
            self.tag_type = getattr(self, "default_tag_type", self._meta.get_field("tag_type").default)

    def __getattr__(self, item):
        """Makes properties of plugin config available as plugin properties.

        A declared entangled field that is not (yet) present in ``config`` resolves to
        its default instead of raising ``AttributeError``. This keeps plugin render code
        (which reads ``instance.<field>`` directly) working for instances that have not
        been through the editing form -- e.g. imported or programmatically built ones --
        while ``clean()`` remains the authoritative place that writes and validates them.
        """
        # 1. Underscore/dunder names are never config fields. Bail first: copy, pickle
        #    and Django internals probe these before ``config`` even exists.
        if item.startswith("_"):
            return super().__getattribute__(item)
        # 2. Read config via __dict__, never self.config -- during unpickle/early init
        #    the field is not set yet and self.config would recurse right here.
        config = self.__dict__.get("config")
        if config is not None and item in config:
            return config[item]
        # 3. Declared entangled field but unset -> its default (a copy, never the shared
        #    cached object). Guarded so resolving the defaults can't re-enter here.
        if not self.__dict__.get("_resolving_defaults"):
            defaults = self._get_config_defaults()
            if item in defaults:
                return copy.deepcopy(defaults[item])
        return super().__getattribute__(item)

    def _get_config_defaults(self):
        """Declared config defaults for this plugin, cached on the (proxy) class."""
        cls = type(self)
        if "_config_defaults_cache" in vars(cls):
            return cls._config_defaults_cache
        self.__dict__["_resolving_defaults"] = True
        try:
            return self._compute_config_defaults()
        finally:
            self.__dict__.pop("_resolving_defaults", None)

    def _compute_config_defaults(self):
        """Resolve the default value of every declared config field.

        Mirrors ``initialize_from_form``: entangled form-field initials, then model-level
        ``default_config``, then settings ``PLUGIN_DEFAULTS``. Returns a partial (and does
        not cache) when the plugin/form cannot be resolved yet (e.g. no ``plugin_type``).
        """
        cls = type(self)
        defaults = {}
        form = None
        if self.__dict__.get("plugin_type"):
            try:
                form = self.get_plugin_class().form
            except Exception:
                form = None
        if form is not None:
            if not getattr(form._meta, "model", None):
                form._meta.model = cls
            try:
                bound = form()
                entangled_fields = getattr(form._meta, "entangled_fields", {}).get("config", ())
                for field in entangled_fields:
                    defaults[field] = {} if field == "attributes" else (bound[field].initial or "")
            except Exception:
                form = None  # incomplete -> don't cache
        for key, value in getattr(cls, "default_config", {}).items():
            defaults[key] = value
        for key, value in PLUGIN_DEFAULTS.get(cls.__name__, {}).items():
            defaults[key] = value
        if form is not None:
            cls._config_defaults_cache = defaults
        return defaults

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
        if SHOW_ADVANCED_SETTINGS:
            attributes = self.config.get("attributes", {})
        else:
            attributes = {}
        classes = self.get_classes()  # get classes
        classes = f'class="{classes}" ' if classes else ""  # to string
        parts = (
            f'{item}="{conditional_escape(value)}"' if value else f"{item}"
            for item, value in attributes.items()
            if item != "class"
        )
        attributes_string = (classes + " ".join(parts)).strip()
        return mark_safe(" " + attributes_string) if attributes_string else ""

    def get_classes(self):
        if SHOW_ADVANCED_SETTINGS:
            attributes = self.config.get("attributes", {})
            classes = set(attributes.get("class", "").split())  # classes added in attriutes
        else:
            classes = set()
        classes.update(self._additional_classes)  # add additional classes
        return conditional_escape(" ".join(classes))

    def save(self, *args, **kwargs):
        self.ui_item = self.__class__.__name__
        return super().save(*args, **kwargs)

    def clean(self):
        """Ensure every declared config field is present, filling missing ones with their
        default. Runs via ``full_clean()``, so an instance built outside the editing form
        (e.g. an import) reaches the same complete, renderable config as an edited one.

        Fill-missing only: existing (user-set) values are never overwritten, so this is
        idempotent and safe to re-run.
        """
        super().clean()
        for key, value in self._get_config_defaults().items():
            self.config.setdefault(key, copy.deepcopy(value))

    def initialize_from_form(self, form=None):
        """Populates the config JSON field based on initial values provided by the fields of form.
        After setting form defaults, applies per-model defaults from the model's ``default_config``
        class attribute (if any), then from the ``DJANGOCMS_FRONTEND_PLUGIN_DEFAULTS`` setting
        (keyed by model class name). Setting-based defaults take highest priority."""
        if form is None:
            form = self.get_plugin_class().form
        if isinstance(form, type):  # if is class
            if not getattr(form._meta, "model", None):
                form._meta.model = self.__class__
            form = form()  # instantiate
        entangled_fields = getattr(getattr(form, "_meta", None), "entangled_fields", {}).get("config", ())
        for field in entangled_fields:
            self.config.setdefault(field, {} if field == "attributes" else form[field].initial or "")
        # Apply model-level defaults (override form defaults)
        for key, value in getattr(self, "default_config", {}).items():
            self.config[key] = value
        # Apply settings-level defaults (highest priority)
        for key, value in PLUGIN_DEFAULTS.get(self.__class__.__name__, {}).items():
            self.config[key] = value
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
