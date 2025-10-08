#########
Reference
#########

********
Settings
********

``djangocms-frontend`` can be configured by putting the appropriate settings
in your project's ``settings.py``.

.. py:attribute:: settings.CMS_COMPONENT_PLUGINS

    Defaults to ``[]``

    A list of dotted pathes to plugin classes that are supposed to also be
    components (see :ref:`components`). Components are plugins to also be
    used in templates using the ``{% plugin %}`` template tag.

    For performance reason, the plugin templates are compiled at startup.

    To make ``djangocms-frontend`` plugins available as components, add the
    following line to your project's settings::

        CMS_COMPONENT_PLUGINS = [
            "djangocms_frontend.cms_plugins.CMSUIPlugin",  # All subclasses are added
            # add other plugins here if needed
        ]


.. py:attribute:: settings.DJANGOCMS_FRONTEND_COMPONENT_FOLDER

    Defaults to ``"cms_components"``

    The subfolder where the component templates are discovered. This is used by the
    :ref:`template components <template_components>` to find the templates
    for the components.

    The folder needs to be created in your app's ``templates/<app_name>/`` directory.
    If you want to use a different folder, set this to the folder name of your choice.

    For example, if you want to use ``"my_components"``, add the following line to your project's settings::

        DJANGOCMS_FRONTEND_COMPONENT_FOLDER = "my_components"

    This causes djangocms-frontend to search for templates on the following paths: ``templates/<app_name>/my_components/``,
    where ``<app_name>`` is the name of any installed app.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_COMPONENT_FIELDS

    Defaults to ``{}``

    A dictionary of installed Django apps and a list of Django form fields to be provided
    to :ref:`template components <template_components>`' context during their registration.
    The form fields can be used with the ``{% field %}`` template tag.

    For example, to add a custom field to the context of all components, add the following line to your project's settings::

        DJANGOCMS_FRONTEND_COMPONENT_FIELDS = {
            "myapp": [
                "myapp.fields.MySuperFieldField",
                "myapp.fields.ChatBotField",
            ],
            # add other apps here if needed
        }

    These fields can be used in the template like this::

        {% field "superField" MySuperFieldField required=True %}
        {% field "chat_bot" ChatBotField required=False %}

    Fields are only imported into the context if the app is installed in the project's ``INSTALLED_APPS``.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_TAG_CHOICES

    Defaults to ``['div', 'section', 'article', 'header', 'footer', 'aside']``.

    Lists the choices for the tag field of all ``djangocms-frontend`` plugins.
    ``div`` is the default tag.

    These tags appear in Advanced Settings of some elements for editors to
    chose from.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_GRID_SIZE

    Defaults to ``12``.



.. py:attribute:: settings.DJANGOCMS_FRONTEND_GRID_CONTAINERS

    Default:

    .. code::

        (
            ("container", _("Container")),
            ("container-fluid", _("Fluid container")),
            ("container-full", _("Full container")),
        )

.. py:attribute:: settings.DJANGOCMS_FRONTEND_USE_ICONS

    Defaults to ``True``.

    Decides if icons should be offered, e.g. in links.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES

    Defaults to ``(('default', _('Default')),)``

    If more than one option is given editors can select which template a
    carousel uses for rendering. Carousel expects the templates in a template
    folder under ``djangocms_frontend/bootstrap5/carousel/{{ name }}/``.
    ``{{ name }}`` denotes the value of the template, i.e. ``default`` in the
    default example.

    Carousel requires at least two files: ``carousel.html`` and ``slide.html``.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_TAB_TEMPLATES

    Defaults to ``(('default', _('Default')),)``

    If more than one option is given editors can select which template a
    tab element uses for rendering. Tabs expects the templates in a template
    folder under ``djangocms_frontend/bootstrap5/tabs/{{ name }}/``.
    ``{{ name }}`` denotes the value of the template, i.e. ``default`` in the
    default example.

    Tabs requires at least two files: ``tabs.html`` and ``item.html``.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_LINK_TEMPLATES

    Defaults to ``(('default', _('Default')),)``

    If more than one option is given editors can select which template a
    link or button element uses for rendering. Link expects the templates in a template
    folder under ``djangocms_frontend/bootstrap5/link/{{ name }}/``.
    ``{{ name }}`` denotes the value of the template, i.e. ``default`` in the
    default example.

    Link requires at least one file: ``link.html``.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_JUMBOTRON_TEMPLATES

    Defaults to ``(('default', _('Default')),)``

    Jumbotrons have been discontinued form Bootstrap 5 (and are not present
    in other frameworks either). The default template mimics the Bootstrap 4's
    jumbotron.

    If more than one option is given editors can select which template a
    jumbotron element uses for rendering. Jumbotron expects the template in a template
    folder under ``djangocms_frontend/bootstrap5/jumbotron/{{ name }}/``.
    ``{{ name }}`` denotes the value of the template, i.e. ``default`` in the
    default example.

    Link requires at least one file: ``jumbotron.html``.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_SPACER_SIZES

    Default:

    .. code::

        (
           ('0', '* 0'),
           ('1', '* .25'),
           ('2', '* .5'),
           ('3', '* 1'),
           ('4', '* 1.5'),
           ('5', '* 3'),
       )

.. py:attribute:: settings.DJANGOCMS_FRONTEND_CAROUSEL_ASPECT_RATIOS

    Default: ``((16, 9),)``

    Additional aspect ratios offered in the carousel component

.. py:attribute:: settings.DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES

    Default:

    .. code::

        (
            ("primary", _("Primary")),
            ("secondary", _("Secondary")),
            ("success", _("Success")),
            ("danger", _("Danger")),
            ("warning", _("Warning")),
            ("info", _("Info")),
            ("light", _("Light")),
            ("dark", _("Dark")),
        )

.. py:attribute:: settings.DJANGOCMS_FRONTEND_ADMIN_CSS

    Default: ``None``

    Adds css format files to the frontend editing forms of
    ``djangocms-frontend``. The syntax is with a ``ModelForm``'s
    ``css`` attribute of its ``Media`` class, e.g.,
    ``DJANGOCMS_FRONTEND_ADMIN_CSS = {"all": ("css/admin.min.css",)}``.

    This css might be used to style have theme-specific colors available
    in the frontend editing forms. The included css file is custom made and
    should only contain color settings in the form of

    .. code-block::

        .frontend-button-group .btn-primary {
            color: #123456;  // add !important here if using djangocms-admin-style
            background-color: #abcdef;
        }

    .. note::

        Changing the ``color`` attribute might require a ``!important`` statement
        if you are using **djangocms-admin-style**.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH

    If unset or smaller than ``1`` the link plugin will render all link options
    into its form. If ``1`` or bigger the link form will wait for the user to
    type at least this many letters and search link targets matching this search
    string using an ajax request.

.. note::

    The following settings of djangocms-picture are respected.

.. py:attribute:: settings.DJANGOCMS_PICTURE_ALIGN

    You can override alignment styles with ``DJANGOCMS_PICTURE_ALIGN``, for example::

        DJANGOCMS_PICTURE_ALIGN = [
            ('top', _('Top Aligned')),
        ]

    This will generate a class prefixed with ``align-``. The example above
    would produce a ``class="align-top"``. Adding a ``class`` key to the image
    attributes automatically merges the alignment with the attribute class.

.. py:attribute:: settings.DJANGOCMS_PICTURE_RATIO

    You can use ``DJANGOCMS_PICTURE_RATIO`` to set the width/height ratio of images
    if these values are not set explicitly on the image::

        DJANGOCMS_PICTURE_RATIO = 1.618

    We use the `golden ratio <https://en.wikipedia.org/wiki/golden_ratio>`_,
    approximately 1.618, as a default value for this.

.. py:attribute:: settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES

    You can enable responsive images technique by setting``DJANGOCMS_PICTURE_RESPONSIVE_IMAGES`` to ``True``.

.. py:attribute:: settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS

    If :py:attr:`~settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES` is set to ``True``,uploaded images will create thumbnails of different sizes according to :py:attr:`~settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS` (which defaults to
    ``[576, 768, 992]``) and browser will be responsible for choosing the best image to display (based upon the
    screen viewport).


.. py:attribute:: settings.DJANGOCMS_PICTURE_TEMPLATES

    This addon provides a ``default`` template for all instances. You can provide
    additional template choices by adding a ``DJANGOCMS_PICTURE_TEMPLATES``
    setting::

        DJANGOCMS_PICTURE_TEMPLATES = [
            ('background', _('Background image')),
        ]

    You'll need to create the `background` folder inside ``templates/djangocms_picture/``
    otherwise you will get a *template does not exist* error. You can do this by
    copying the ``default`` folder inside that directory and renaming it to
    ``background``.


.. py:attribute:: settings.TEXT_SAVE_IMAGE_FUNCTION

    If you want to use
    djangocms-text-ckeditor's `Drag & Drop Images
    <https://github.com/django-cms/djangocms-text-ckeditor/#drag--drop-images>`_
    so be sure to set ``TEXT_SAVE_IMAGE_FUNCTION``::

      TEXT_SAVE_IMAGE_FUNCTION = 'djangocms_frontend.contrib.image.image_save.create_image_plugin'

    Otherwise set ``TEXT_SAVE_IMAGE_FUNCTION = None``

.. py:attribute:: settings.DJANGOCMS_FRONTEND_ICON_LIBRARIES

    Default::

        DJANGOCMS_FRONTEND_ICON_LIBRARIES = {
            'font-awesome': (
                'font-awesome.min.json',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
            ),
            'bootstrap-icons': (
                'bootstrap-icons.min.json',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css'
             ),
            'material-icons-filled': (
                'material-icons-filled.min.json',
                'https://fonts.googleapis.com/css2?family=Material+Icons'
            ),
            ...

    For each available icon set there is an entry in this dictionary. The key is the basis for the displayed name. The value is a 2-tuple:

    1. The name of the config file which is a static file with the path ``djangocms_frontend/icon/vendor/assets/icon-libraries/``.
    2. The name of the css file defining the icons. It is either a path or a file name. If it is a file name the css file is fetched from ``djangocms_frontend/icon/vendor/assets/stylesheets/``.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_ICON_LIBRARIES_SHOWN

    Default::

        DJANGOCMS_FRONTEND_ICON_LIBRARIES_SHOWN = (
            "font-awesome",
            "bootstrap-icons",
            "material-icons-filled",
            "material-icons-outlined",
            "material-icons-round",
            "material-icons-sharp",
            "material-icons-two-tone",
            "fomantic-ui",
            "foundation-icons",
            "elegant-icons",
            "feather-icons",
            "open-iconic",
            "tabler-icons",
            "weather-icons",
        )

    This settings allows to restrict the number of icon sets shown to the user. Typically one or two icon sets should be sufficient to keep a consistent icon expierence.

    .. warning::

        This setting only has an effecet if :py:attr:`~settings.DJANGOCMS_FRONTEND_ICON_LIBRARIES` is not explicitly set.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_ICON_SIZE_CHOICES

    Default::

        DJANGOCMS_FRONTEND_ICON_SIZE_CHOICES = (
            ("", _("Regular")),
            ("200%", _("x 2")),
            ("300%", _("x 3")),
            ("400%", _("x 4")),
            ("500%", _("x 5")),
            ("800%", _("x 8")),
            ("1200%", _("x 12")),
        )

    This lost of options define the icon size choices a user can select. The values (first tuple element) are css units for the ``font-size`` css property. Besides relative units (``%``) any css unit can be used, e.g. ``112pt``.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_SHOW_EMPTY_CHILDREN

    Default: ``False``

    If set to ``True`` the frontend editing will show a message where children
    can be added to plugins to complete the design. This is supposed to make
    the editing experience more intuitive for editors.


******
Models
******

``djangocms-frontend`` subclasses the ``CMSPlugin`` model.

.. py:class:: FrontendUIItem(CMSPlugin)

    Import from ``djangocms_frontend.models``.

    All concrete models for UI items are proxy models of this class.
    This implies you can create, delete and update instances of the proxy models
    and all the data will be saved as if you were using this original
    (non-proxied) model.

    This way all proxies can have different python methods as needed while still
    all using the single database table of ``FrontendUIItem``.

.. py:attribute:: FrontendUIItem.ui_item

    This CharField contains the UI item's type without the suffix "Plugin",
    e.g. "Link" and not "LinkPlugin". This is a convenience field. The plugin
    type is determined by ``CMSPlugin.plugin_type``.

.. py:attribute:: FrontendUIItem.tag_type

    This is the tag type field determining what tag type the UI item should have.
    Tag types default to ``<div>``.

.. py:attribute:: FrontendUIItem.config

    The field ``config`` is the JSON field that contains a dictionary with all specific
    information needed for the UI item. The entries of the dictionary can be
    directly **read** as attributes of the ``FrontendUIItem`` instance. For
    example, ``ui_item.context`` will give ``ui_item.config["context"]``.

    .. warning::

        Note that changes to the ``config`` must be written directly to the
        dictionary:  ``ui_item.config["context"] = None``.


.. py:method:: FrontendUIItem.add_classes(self, *args)

    This helper method allows a Plugin's render method to add framework-specific
    html classes to be added when a model is rendered. Each positional argument
    can be a string for a class name or a list of strings to be added to the list
    of html classes.

    These classes are **not** saved to the database. They merely a are stored
    to simplify the rendering process and are lost once a UI item has been
    rendered.

.. py:method:: FrontendUIItem.get_attributes(self)

    This method renders all attributes given in the optional ``attributes``
    field (stored in ``.config``). The ``class`` attribute reflects all
    additional classes that have been passed to the model instance by means
    of the ``.add_classes`` method.

.. py:method:: FrontendUIItem.initialize_from_form(self, form)

    Since the UIItem models do not have default values for the contents of
    their ``.config`` dictionary, a newly created instance of an UI item
    will not have config data set, not even required data.

    This method initializes all fields in ``.config`` by setting the value to
    the respective ``initial`` property of the UI items admin form.

.. py:method:: FrontendUIItem.get_short_description(self)

    returns a plugin-specific short description shown in the structure mode
    of django CMS.

************
Form widgets
************

``djangocms-frontend`` contains button group widgets which can be used as
for ``forms.ChoiceField``. They might turn out helpful when adding custom
plugins.

.. py:class:: ButtonGroup(forms.RadioSelect)

    Import from ``djangocms_frontend.fields``

    The button group widget displays a set of buttons for the user to chose. Usable for up
    to roughly five options.

.. py:class:: ColoredButtonGroup(ButtonGroup)

    Import from ``djangocms_frontend.fields``

    Used to display the context color selection buttons.

.. py:class:: IconGroup(ButtonGroup)

    Import from ``djangocms_frontend.fields``.

    This widget displays icons in stead of text for the options. Each icon is rendered
    by ``<span class="icon icon-{{value}}"></span>``. Add css in the ``Media``
    subclass to ensure that for each option's value the span renders the
    appropriate icon.

.. py:class:: IconMultiselect(forms.CheckboxSelectMultiple)

    Import from ``djangocms_frontend.fields``.

    Like ``IconGroup`` this widget displays a choice of icons. Since it inherits
    from ``CheckboxSelectMultiple`` the icons work like checkboxes and not radio
    buttons.

.. py:class:: OptionalDeviceChoiceField(forms.MultipleChoiceField)

    Import from ``djangocms_frontend.fields``.

    This form field displays a choice of devices corresponding to breakpoints
    in the responsive grid. The user can select any combination of devices
    including none and all.

    The result is a list of values of the selected choices or None for all devices
    selected.

.. py:class:: DeviceChoiceField(OptionalDeviceChoiceField)

    Import from ``djangocms_frontend.fields``.

    This form field is identical to the ``OptionalDeviceChoiceField`` above,
    but requires the user to select at least one device.

*******************
Management commands
*******************

Management commands are run by typing ``python -m manage frontend command`` in the
project directory. ``command`` can be one of the following:

``migrate``
    Migrates plugins from other frontend packages to ``djangocms-frontend``.
    Currently supports **djangocms_bootstrap4** and **djangocms_styled_link**.
    Other packages can be migrated adding custom migration modules to
    the ``DJANGOCMS_FRONTEND_ADDITIONAL_MIGRATIONS`` setting.

``stale_references``
    If references in a UI item are moved or removed the UI items are designed to
    fall back gracefully and both not throw errors or be deleted themselves
    (by a db cascade).

    The drawback is, that references might become stale. This command prints all
    stale references, their plugins and pages/placeholder they belong to.

.. _sync_permissions:

``sync_permissions``
    This command syncs permissions for users or groups. It is run with one of
    the following arguments:

    - ``users``: Syncs permissions for all users.
    - ``groups``: Syncs permissions for all groups.

    Permissions are copied from the ``FrontendUIItem`` model to all installed
    plugins. This way you can set permissions for all plugins by setting them
    for ``FrontendUIItem`` and then syncing them.


*************
Running Tests
*************

You can run tests by executing:

.. code::

   python -m venv env
   source env/bin/activate
   pip install -r tests/requirements/base.txt
   pytest

