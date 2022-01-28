Why djangocms-frontend
======================

Django CMS introduces a separation between content editors and developers.
In a nutshell, developers provide needed functionality and
content editors focus on using this functionality to
present the desired content.

``djangocms-frontend`` aims to provide plugins for modern, responsive
web designs while abstracting from the specific css framework used to
implement these design. Content editor should not need to care, e.g., what
version of Bootstrap is used, or if Bootstrap is used at all.

If developers decide upgrade a css framework from one version to another, or
even to another framework, content editors should not have to rebuild their
content.


Functionality
=============

``djangocms-frontend`` adds a set of plugins to Django-CMS to allow for quick
usage of components defined by the underlying css framework, e.g. bootstrap 5.

`Accordion <https://getbootstrap.com/docs/5.0/components/accordion/>`_

Alert component
---------------

`Alerts <https://getbootstrap.com/docs/5.0/components/alerts/>`_

Badge component
---------------

`Badge <https://getbootstrap.com/docs/5.0/components/badge/>`_

Card component
--------------
`Card <https://getbootstrap.com/docs/5.0/components/card/>`_

Carousel component
------------------
A `Carousel <https://getbootstrap.com/docs/5.0/components/carousel/>`_ is a set of
images (pontentially with some description) that slide in (or fade in) one
after the other after a certain amount of time.

Collapse component
------------------
The `Collapse <https://getbootstrap.com/docs/5.0/components/collapse/>`_ hides text
behind its headline and offers the user a trigger (e.g., a button) to reveal itself.




* `Content (Blockquote, Code, Figure) <https://getbootstrap.com/docs/5.0/content/>`_
* `Grid (Container, Row, Column) <https://getbootstrap.com/docs/5.0/layout/grid/>`_
* `Jumbotron <https://getbootstrap.com/docs/5.0/components/jumbotron/>`_
* `Link / Button <https://getbootstrap.com/docs/5.0/components/buttons/>`_
* `List group <https://getbootstrap.com/docs/5.0/components/list-group/>`_
* `Media <https://getbootstrap.com/docs/5.0/layout/media-object/>`_
* `Picture / Image <https://getbootstrap.com/docs/5.0/content/images/>`_
* `Tabs <https://getbootstrap.com/docs/5.0/components/navs/#tabs>`_
* `Utilities (Spacing) <https://getbootstrap.com/docs/5.0/utilities/>`_
