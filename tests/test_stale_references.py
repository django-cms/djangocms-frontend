from io import StringIO

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.core.management import call_command

from djangocms_frontend.contrib.alert.models import Alert

from .fixtures import DJANGO_CMS4, TestFixture

STALE = {"model": "cms.page", "pk": 99999}


class StaleReferencesCommandTestCase(TestFixture, CMSTestCase):
    """Tests for the frontend stale_references management command."""

    def _call_stale_references(self, **kwargs):
        out = StringIO()
        err = StringIO()
        call_command("frontend", "stale_references", stdout=out, stderr=err, **kwargs)
        return out.getvalue(), err.getvalue()

    def _add_link(self, config, placeholder=None):
        return add_plugin(
            placeholder or self.placeholder,
            "TextLinkPlugin",
            self.language,
            config=config,
        )

    def test_no_stale_references(self):
        """A plugin pointing at an existing object is not reported."""
        self._add_link({"internal_link": {"model": "cms.page", "pk": self.home.pk}})

        out, err = self._call_stale_references()

        self.assertNotIn("stale field", out)
        self.assertIn("Finished checking references", out)
        self.assertEqual(err, "")

    def test_stale_reference_on_page_is_reported(self):
        """A dangling reference is reported together with the placeholder's source object."""
        plugin = self._add_link({"internal_link": STALE})

        out, err = self._call_stale_references()

        self.assertIn(f"Link (pk={plugin.pk}) stale field internal_link.", out)
        if DJANGO_CMS4:
            source = self.placeholder.source
            self.assertIn(f'... in {source} (placeholder "{self.placeholder.slot}")', out)
        else:  # django CMS 3 placeholders have no source object
            self.assertIn(f"... in placeholder #{self.placeholder.pk}", out)
        self.assertEqual(err, "")

    def test_stale_reference_without_placeholder(self):
        """Plugins that are not in any placeholder do not crash the command."""
        instance = Alert.objects.create(config={"alert_link": STALE})

        out, _ = self._call_stale_references()

        self.assertIn(f"(pk={instance.pk}) stale field alert_link.", out)
        self.assertIn("... not in any placeholder (orphaned plugin)", out)

    def test_stale_reference_in_detached_placeholder(self):
        """A placeholder not attached to a page is reported by its own pk."""
        from cms.models import Placeholder

        placeholder = Placeholder.objects.create(slot="detached")
        plugin = self._add_link({"internal_link": STALE}, placeholder=placeholder)

        out, _ = self._call_stale_references()

        self.assertIn(f"Link (pk={plugin.pk}) stale field internal_link.", out)
        self.assertIn(f"... in placeholder #{placeholder.pk}", out)

    def test_non_reference_config_is_ignored(self):
        """Config values that are not model references are left alone."""
        self._add_link({"attributes": {"class": "btn"}, "target": ""})

        out, _ = self._call_stale_references()

        self.assertNotIn("stale field", out)
        self.assertIn("Finished checking references", out)
