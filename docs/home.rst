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


