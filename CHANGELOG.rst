=========
Changelog
=========

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


