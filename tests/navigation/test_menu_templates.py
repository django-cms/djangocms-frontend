import re

from cms.test_utils.testcases import CMSTestCase
from django.template import RequestContext, Template

from ..fixtures import TestFixture

MENU_TEMPLATES = (
    "bootstrap5/menu.html",
    "djangocms_frontend/bootstrap5/navigation/default/menu.html",
    "djangocms_frontend/bootstrap5/navigation/offcanvas/menu.html",
)


class MenuTemplateTestCase(TestFixture, CMSTestCase):
    def setUp(self):
        super().setUp()
        self.child = self.create_page(
            title="child",
            template="page.html",
            parent=self.page,
        )
        self.publish(self.page, self.language)
        self.publish(self.child, self.language)

    def tearDown(self):
        self.child.delete()
        return super().tearDown()

    def render_menu(self, template):
        request = self.get_request(self.page.get_absolute_url(self.language), page=self.page)
        return Template('{% load menu_tags %}{% show_menu 0 100 100 100 "' + template + '" %}').render(
            RequestContext(request)
        )

    def test_dropdown_aria_labelledby_matches_toggle_id(self):
        """The dropdown's aria-labelledby must reference the id of its toggle. Regression test
        for the ``child.ancestor.id`` typo, which always rendered an empty ``menu-`` reference."""
        for template in MENU_TEMPLATES:
            with self.subTest(template=template):
                html = self.render_menu(template)

                toggle_ids = re.findall(r'\bid="menu-([^"]*)"', html)
                labelled_by = re.findall(r'\baria-labelledby="menu-([^"]*)"', html)

                self.assertTrue(toggle_ids, "no menu toggle rendered")
                self.assertTrue(labelled_by, "no dropdown rendered")
                for value in labelled_by:
                    self.assertNotEqual(value, "", "aria-labelledby references an empty id")
                    self.assertIn(value, toggle_ids)
