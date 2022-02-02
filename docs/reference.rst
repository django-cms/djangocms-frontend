###########
 Reference
###########

**********
 Settings
**********

Available settings will be revised. For now only the following can be
changed:

.. code::

   DJANGOCMS_FRONTEND_TAG_CHOICES = ['div', 'section', 'article', 'header', 'footer', 'aside']

   DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES = (
       ('default', _('Default')),
   )

   DJANGOCMS_FRONTEND_GRID_SIZE = 12
   DJANGOCMS_FRONTEND_GRID_CONTAINERS = (
       ('container', _('Container')),
       ('container-fluid', _('Fluid container')),
       ("container-sm", _("sx container")),
       ("container-md", _("md container")),
       ("container-lg", _("lg container")),
       ("container-xl", _("xl container")),
   )

   DJANGOCMS_FRONTEND_USE_ICONS = True

   DJANGOCMS_FRONTEND_TAB_TEMPLATES = (
       ('default', _('Default')),
   )

   DJANGOCMS_FRONTEND_SPACER_SIZES = (
       ('0', '* 0'),
       ('1', '* .25'),
       ('2', '* .5'),
       ('3', '* 1'),
       ('4', '* 1.5'),
       ('5', '* 3'),
   )

   DJANGOCMS_FRONTEND_CAROUSEL_ASPECT_RATIOS = (
       (16, 9),
   )

   DJANGOCMS_BOOTSTRAP5_COLOR_STYLE_CHOICES = (
       ('primary', _('Primary')),
       ('secondary', _('Secondary')),
       ('success', _('Success')),
       ('danger', _('Danger')),
       ('warning', _('Warning')),
       ('info', _('Info')),
       ('light', _('Light')),
       ('dark', _('Dark')),
       ('custom', _('Custom')),
   )

Please be aware that this package does not support
djangocms-text-ckeditor's `Drag & Drop Images
<https://github.com/divio/djangocms-text-ckeditor/#drag--drop-images>`_
so be sure to set ``TEXT_SAVE_IMAGE_FUNCTION = None``.

***************
 Running Tests
***************

You can run tests by executing:

.. code::

   virtualenv env
   source env/bin/activate
   pip install -r tests/requirements.txt
   python setup.py test

To run the frontend make sure to use **node 10.x**.
