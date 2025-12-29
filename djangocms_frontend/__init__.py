"""
See PEP 440 (https://www.python.org/dev/peps/pep-0440/)

Release logic:
 1. Increase version number (change __version__ below).
 2. Ensure the static bundle is upto date with ``nvm use && npm install && gulp sass && gulp bundle``
 3. Assure that all changes have been documented in CHANGELOG.rst.
 4. In setup.py check that
   - versions from all third party packages are pinned in ``REQUIREMENTS``.
   - the list of ``CLASSIFIERS`` is up-to-date.
 5. git add djangocms_frontend/__init__.py CHANGELOG.rst setup.py
 6. run ``django-admin compilemessages`` from the ``djangocms_frontend`` folder
 7. git add all changed .mo files
 8. git commit -m 'Bump to {new version}'
 9. git push
10. Assure that all tests pass on https://github.com/django-cms/djangocms-frontend/actions
11. Create a new release on https://github.com/django-cms/djangocms-frontend/releases/new
12. Publish the release when ready
13. Github actions will publish the new package to pypi
"""

__version__ = "2.3.0"
