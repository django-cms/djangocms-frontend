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
