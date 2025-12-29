import sys
from unittest import skipIf

from django.test.testcases import TestCase


@skipIf(sys.version_info < (3, 10), "Python 3.10 or higher required")
class LinkMigrationTestCase(TestCase):
    def setUp(self):
        import importlib

        link_migration = importlib.import_module("djangocms_frontend.migrations.0002_migrate_links")
        self.convert = staticmethod(link_migration.convert_item)

    def test_link_migration(self):
        test_links = (
            dict(external_link="https://www.django-cms.com"),
            dict(external_link="https://www.django-cms.com", anchor="top"),
            dict(internal_link=dict(model="cms.page", pk=1)),
            dict(internal_link=dict(model="cms.page", pk=1), anchor="top"),
            dict(file_link=dict(model="filer.file", pk=1)),
            dict(phone="1234567890"),
            dict(mailto="mail@example.com"),
        )

        for link in test_links:
            with self.subTest(link=link):
                config = link.copy()
                self.convert(config, "forward")
                self.convert(config, "backward")
                self.assertEqual(link, config)
