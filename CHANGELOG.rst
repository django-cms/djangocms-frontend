=========
Changelog
=========

1.3.2 (2024-04-25)
==================

* fix: make grid layout (rows/columns) compatible with flex box-based Django admin by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/208
* fix: Improved handling of optional smart link field by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/210


1.3.1 (2024-04-12)
==================

* fix: Allow page titles to contain ampersand (&) by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/202
* fix: Use gettext_lazy for model verbose names by @tidenhub in https://github.com/django-cms/djangocms-frontend/pull/203
* fix: Add `dir` attribute to `html` tag in `djangocms_frontend.html` by @sakhawy in https://github.com/django-cms/djangocms-frontend/pull/204

**New Contributors**

* @tidenhub made their first contribution in https://github.com/django-cms/djangocms-frontend/pull/203
* @sakhawy made their first contribution in https://github.com/django-cms/djangocms-frontend/pull/204

1.3.0 (2024-03-21)
==================

* feat: Add abstract base model `AbstractFrontendUIItem` by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/195
* feat: Add icons for selected text-enabled plugins by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/195
* fix: Correct site used when using Link plugin within a static placholder in django CMS 3.x by @fsbraun
* fix: removed Nav Container plugin and fixed Navigation Link plugin by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/192
* fix: Remove `{% spaceless %}` around `{% block "content" %}` by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/188
* fix: Improved fieldset layout for Django 4.2+ by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/185
* fix: Dropped django-select2 dependency


1.2.2 (2024-01-13)
==================

* fix: Reference to removed icon fonts caused some static file storage backends to fail
* fix: Replace deprecated ``length_is`` by ``length`` filter by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/173
* fix: Missing space in auto column short description by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/177
* docs: Update how tos by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/174
* docs: Typo corrections by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/175
* docs: Clarify how to re-use image and links in custom plugins by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/176
* ci: pre-commit autoupdate by @pre-commit-ci in https://github.com/django-cms/djangocms-frontend/pull/172
* ci: bump github/codeql-action from 2 to 3 by @dependabot in https://github.com/django-cms/djangocms-frontend/pull/171

1.2.1 (2023-12-20)
==================

* feat: Add licences of vendor icon libraries by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/167
* feat: django 5.1 preparation by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/169
* fix: Button group sizes for django 4.x+ by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/170
* ci:(deps): bump actions/setup-python from 4 to 5 by @dependabot in https://github.com/django-cms/djangocms-frontend/pull/168



1.2.0 (2023-11-28)
==================

* feat: Add float option for images by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/162
* feat: Add drag'n'drop support for djangocms-text-ckeditor by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/165
* fix: Ckeditor does not show icons for editing by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/163
* fix: Replace ``stylesSet`` setting in docs with ``customConfig` for icons in ckeditor by @fsbraun in https://github.com/django-cms/djangocms-frontend/pull/164
* ci: pre-commit autoupdate by @pre-commit-ci in https://github.com/django-cms/djangocms-frontend/pull/161


1.1.10 (2023-10-23)
===================

* Fix bug: icon template tags do not throw an exception if called with
  empty icon
* Rename "Template" fields to "Layout"
* Fix bug: Card image at top of card recognized also for django CMS v4
* Fix bug: Picture ratio retained for image plugin
* Fix bug: Show selected page in menu of default template.

1.1.7 (2023-08-03)
==================

* Fix bug: set proper image target link in template
* Feature: Add Spanish translations

1.1.6 (2023-07-26)
==================

* Fix incomplete migration of code plugins from djangocms-bootstrap4
* Add compiled French locale (*.mo)
* Add partial Dutch locale

1.1.5 (2023-07-14)
==================

* Fix bug where url for link select2 field was lost after app hook reload (#135)
* Use `bg-body` class on Bootstrap 5's tab navigation to support color modes (#138)
* Fix styling of icon buttons for better usager with plain django admin style (#141)

1.1.4 (2023-05-28)
==================

* Fix css issues

1.1.3 (2023-05-26)
==================

* Add: Image is not text-enabled
* Fix row and column admin style to work with Django admin themes that use flexbox.

1.1.2 (2023-04-25)
==================

* Fix asset loading for icon picker with whitenoise or other static file servers


1.1.1
=====

* Django 4.2 compatibility
* Allow accordion header size to unset resulting in an accordion item header with
  standard size (#119).
* Fix a bug that overwrote image sizes by 640x400 if both width and height were given (#117).
* Update of docs on how to correctly see IconPlugin instances in CKEDITOR (#115)
* Add ruff as linter

1.1.0
=====

* Add djangocms_frontend.contrib.icon
* Fix a bug which lets a carousel not start on django CMS 4.0+
* Update translations
* Add tests for Django 4.2

1.0.2
=====

* Add missing form mixin for link plugin (allowing it to be extended)
* Fix Link template choices from correct setting
* Improve carousel form, remove illegal options for Bootstrap 5

1.0.1
=====

* Add Django 4.0, 4.1 and Python 3.10, 3.11 support
* Remove superfluous space in some tags
* Fix figure and blockquote caption
* Fix HTML injection security bug
* Removed caption from Image plugin (use figure instead)
* Fixed js bug for icon preview

1.0.0
=====

* Fix packages.json, gulpfile.js to allow automatic build of js and css
* Fix accordion markup
* Fix dark mode for select2 widget
* Fix lint errors in scss files
* removed forms app
* Minor docs corrections
* For the boostrap5 base template include bootstrap v5.2.1, jQuery 3.6.1
* Base template respects admin color scheme
* Fix for ``Image`` plugin where the associated ``filer.Image`` has been deleted.

0.9.4
=====

* Refactor forms app into independent project
* Deprecation warning for forms app
* Add dark mode compatibility with django CMS 3.11
* Remove strong dependency on djangocms-icon
* Sync github and pypi releases

0.9.1
=====

* Added forms app
* Several bux fixes

0.9.0
=====

* Added shadow options for containers, cards, alerts, ...
* Added background color and opacity options for containers and cards
* Added management command `stale_frontend_references` to identify stale
  references (e.g., images, links)
* Added icons for tab alignment
* Added Tabs edit UI for simpler edit
* Introduced Mixins (for advanced settings, first)


0.2.0
=====

* First release on Pypi

0.1.0 (unreleased)
==================

* Bootstrap 5
* Based on djangocms-bootstrap5 0.1.0
* Changes to naming for djangocms_framework
* Refactor to separate frontend from framework elements
* Unify models to one single table with a json field to contain plugin-
  specific data (based an django-entangled)
* Added accordion plugins
* New link plugin with ability to link to internal pages from other apps than
  django CMS
* New image plugin to remove dependency from djangocms-picture
* Add migration management command to migrate djangocms-bootstrap4 plugins to
  django-framework plugins
* Fixed templates to match bootstrap5 specs (removing some incompatibilities)
* Replaced discontinued jumbotron and media  with valid bootstrap 5
  templates
* Added bootstrap 5's new xxl breakpoint


