.. _how to add internal link targets outside of the cms:

**************************************************
 How to add internal link targets outside the CMS
**************************************************

As of version 2 of ``djangocms-frontend``, the link/button plugin builds upon
the ``LinkFormField`` of djangocms-link. djangocms-link uses Django admin to
autodetect linkable models. This means that any model that has a
``get_absolute_url()`` method and a ``search_fields`` attribute in its
``ModelAdmin`` will be available as an internal link target.

The ``DJANGOCMS_FRONTEND_LINK_MODELS`` setting in ``djangocms-frontend`` before
version 2 does not have any effect anymore.

See the README file of `djangocms-link <https://github.com/django-cms/djangocms-link/blob/master/README.rst>`_
for more information.

