from unittest import skipIf

from cms.test_utils.testcases import CMSTestCase
from cms.utils.apphook_reload import reload_urlconf
from django.urls import NoReverseMatch, reverse

from djangocms_frontend.contrib.link.forms import LinkForm
from tests.fixtures import DJANGO_CMS4, TestFixture


@skipIf(DJANGO_CMS4, "Tests for django CMS 4 use URL manager with own select2")
class TestUrlConfTestCase(TestFixture, CMSTestCase):
    def test_select2_url_reversible(self):
        try:
            reverse("dcf_autocomplete:ac_view")
        except NoReverseMatch as e:
            self.fail(str(e))

    def test_select2_url_robust_after_url_reload(self):
        # reload url but do not execute AppConfig.ready() where
        reload_urlconf()

        # Check url is gone
        with self.assertRaises(NoReverseMatch):
            reverse("dcf_autocomplete:ac_view")

        form = LinkForm()
        form.request = None
        str(form)  # renders form

        # Now does not fail
        try:
            reverse("dcf_autocomplete:ac_view")
        except NoReverseMatch as e:
            self.fail(str(e))
