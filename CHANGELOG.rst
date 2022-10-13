=========
Changelog
=========

* Add Django 4.0, 4.1 and Python 3.10 support
* Remove superfluous space in some tags
* Fix figure and blockquote caption
* Fix HTML injection security bug
* Removed caption from Image plugin (use figure instead)
* Fixed js bug for icon preview


1.0.0
==========
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


