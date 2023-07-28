=========
Changelog
=========

unpublished
===========

* Fix bug: set proper image target link in template

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


