from unittest import skipIf

from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse
from django.urls import NoReverseMatch

from tests.fixtures import DJANGO_CMS4, TestFixture


@skipIf(DJANGO_CMS4, "Tests for django CMS 4 use URL manager with own select2")
class TestUrlConfTestCase(TestFixture, CMSTestCase):
    def test_select2_url_reversible(self):
        try:
            admin_reverse("link_link_autocomplete")
        except NoReverseMatch as e:
            self.fail(str(e))
