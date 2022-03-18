To test your app against django CMS version 4 you will need to adjsut tests.

Frist, we for the time being recommend to following requirements for django CMS
v4 (development version) for the Django and django CMS part:

. code::

    Django>=3.2,<4.0
    -e git+https://github.com/django-cms/django-cms.git@develop-4#egg=django-cms
    -e git+https://github.com/Aiky30/djangocms-alias.git@feature/django-32-compat#egg=djangocms-alias
    -e git+https://github.com/django-cms/djangocms-url-manager.git@master#egg=djangocms-url-manager
    https://github.com/django-cms/djangocms-versioning/tarball/master#egg=djangocms-versioning
    -e git+https://github.com/FidelityInternational/djangocms-pageadmin.git@1.0.0#egg=djangocms-pageadmin
    -e git+https://github.com/FidelityInternational/djangocms-version-locking.git@master#egg=djangocms-version-locking

You might have to adjust your fixtures to differentiate test for django CMS v3
and django CMS v4.

To determine if tests are run against v3 or v4, add this to your test settings
(this assumes the above requiremets):

. code::

    try:  # V4 test?
        import djangocms_versioning

        INSTALLED_APPS += [
            "djangocms_versioning",
            "djangocms_alias",
            "djangocms_url_manager",
            "djangocms_pageadmin",
            "djangocms_version_locking",
        ]
    except ImportError:  # Nope
        pass

Then you can differentiate your fixtures by doing this:

    from django.apps import apps

    DJANGO_CMS4 = apps.is_installed("djangocms_versioning")



Key differences to test against v3 and v4 are:

page.placeholders
    ``page.palceholders`` is not present in django CMS v4. Use ``page.get_placeholders(language)``
    instead. Note, however, that in v4 ``page.get_placeholders(language)`` requires
    the language parameter while in v3 it must not be present. A solution can
    be to add a method ``get_placeholders`` to your test class that calls
    the page's method with or without the language parameter depending on which
    version you are testing with.

page.publish
page.unpublish
    In django CMS v4 the ``Page`` model does not have ``.publish`` or ``.unpublish``
    methods. Publication is handleded by djangocms-versioning. This requires to
    find all versions of a page and identifying the current draft version to
    publish or the current published version to unpublish. For an example
    code fragment see below.

create_page:
    The CMS function ``crate_page`` needs additional arguments in v4:

    * ``created_by``: User who creates the page. Can often be ``self.superuser``
    * ``in_navigation``: Can default to ``True``
    * ``limit_visibility_in_menu``: Can default to ``None``



We add the following code fragment to our mixtures:

.. code:: python

    if DJANGO_CMS4:  # CMS V4

        def _get_version(self, grouper, version_state, language=None):
            language = language or self.language

            from djangocms_versioning.models import Version

            versions = Version.objects.filter_by_grouper(grouper).filter(
                state=version_state
            )
            for version in versions:
                if (
                    hasattr(version.content, "language")
                    and version.content.language == language
                ):
                    return version

        def publish(self, grouper, language=None):
            from djangocms_versioning.constants import DRAFT

            version = self._get_version(grouper, DRAFT, language)
            if version is not None:
                version.publish(self.superuser)

        def unpublish(self, grouper, language=None):
            from djangocms_versioning.constants import PUBLISHED

            version = self._get_version(grouper, PUBLISHED, language)
            if version is not None:
                version.unpublish(self.superuser)

        def create_page(self, title, **kwargs):
            kwargs.setdefault("language", self.language)
            kwargs.setdefault("created_by", self.superuser)
            kwargs.setdefault("in_navigation", True)
            kwargs.setdefault("limit_visibility_in_menu", None)
            kwargs.setdefault("menu_title", title)
            return create_page(
                title=title,
                **kwargs
            )

        def get_placeholders(self, page):
            return page.get_placeholders(self.language)

    else:  # CMS V3

        def publish(self, page, language=None):
            page.publish(language)

        def unpublish(self, page, language=None):
            page.unpublish(language)

        def create_page(self, title, **kwargs):
            kwargs.setdefault("language", self.language)
            kwargs.setdefault("menu_title", title)
            return create_page(
                title=title,
                **kwargs
            )

        def get_placeholders(self, page):
            return page.get_placeholders()
