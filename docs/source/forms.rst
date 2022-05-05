#######
 Forms
#######

.. note::

    Forms a available as of version 0.9.1

.. warning::

    Currently, for forms to work they require **jQuery** to be installed by
    the user.


**djangocms-frontend** supports rendering of styled forms which is part of
all major frontend frameworks, like Bootstrap 5. The objective is to tightly
integrate forms in the website design. Djangocms-frontend allows as many forms
as you wish on one page. All forms are **ajax/xhr-based**. To this end,
djangocms-frontend extends the django CMS plugin model allowing a form plugin
to receive ajax post requests.

There are two different ways to manage forms with **djangocms-frontend**:

1. **Building a form with django CMS' powerful structure board.** This is
   fast an easy. It integrates smoothly with other design elements, especially
   the grid elements allowing to design simple responsive forms.

   Form actions can be configured by form. Built in actions include saving the
   results in the database for later evaluation and mailing submitted forms to
   the site admins. Other form actions can be registered.

   If you prefer to have a central form repository, we suggest
   **djangocms-alias** to manage your forms centrally. Djangocms-alias becomes
   your form editors and forms can be placed on pages by refering to them with
   their alias.

2. **Registering an application-specific form with djangocms-frontend.** If you
   already have forms you may register them with djangocms-frontend and allow
   editors to use them in the form plugin. If you use
   `django-crispy-forms <https://github.com/django-crispy-forms/django-crispy-forms>`_
   all form layouts will be retained. If you only have simpler design
   requirements, **djangocms-frontend** allows you to use fieldsets as with
   admin forms.

**************
Building forms
**************

Form plugin
===========

All forms live in the Form plugin. A form plugin can be positioned everywhere
except inside another form plugin.

If you want to use the structure board to build your form you will have to add
the form components as child plugins to a form plugin. If you have registiered
an application-specific form with djangocms-frontend you will be able to select
one of the registered forms for be shown by the form plugin. (If you do both,
the selected form takes precedence over the child plugins.)

.. image:: screenshots/form-plugin.png
    :width: 720

In the tab "Submit button" the name and appearance of the submit button is
configured.


Form fields
===========

The form plugin accepts all regular plugins **plus** special plugins that
represent form fields. These are:

* Text
* Textarea
* Integer
* Decimal
* Boolean
* Date
* Time
* Date and Time
* Select/Choice
* URL
* Email

Each field requires an input of then specific form. Some fields (e.g., Boolean
or Select/Choice) offer options on the specific input widget.

Djangocms frontend will use framework specific widgets or fall back to standard
widgets browsers offer (e.g., date picker).

***************************
Using forms from other apps
***************************

Other apps can register forms to be used by **djangocms-frontend**. Once at
least one form is registered, the form will appear as a option in the Form
plugin.

Registration is can simply be done by a decorator or function call:

.. code:: python

    from django import forms
    from djangocms_frontend.contrib.frontend_forms import register_with_frontend

    @register_with_frontend
    class MyCoolForm(forms.Form):
        ...

    class MyOtherCoolForm(forms.Form):
        ...

    register_with_frontend(MyOtherCoolForm)



There are three ways **djangocms-frontend** can render registered forms:

1. **Regular form rendering**: all fields a shown below one another. This is
   only advisable for very simple forms (e.g. a contact form with name, email,
   and text body).

2. **Adding a fieldsets argument to the form**: The ``fieldsets`` work as you
   know them from ``ModelAdmin``. See `Django documentation
   <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets>`_.
   This may be the most convenient way of building not-too-complex forms.
   **djangocms-frontend** uses the grid system to generate the form layout.

3. **Using the third party package** `django-crispy-forms <https://github.com/django-crispy-forms/django-crispy-forms>`_:
   If installed and the form has a property ``helper`` the form is automatically
   rendered using **django-crispy-forms**. Note, however, that the submit button
   is rendered by the plugin. Hence do not include it into the form (which is
   possible with **django-crispy-forms**).

