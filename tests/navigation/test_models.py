from django.test import TestCase

from djangocms_frontend.contrib.navigation.forms import (
    NavigationForm,
    NavLinkForm,
    PageTreeForm,
)
from djangocms_frontend.contrib.navigation.models import Navigation, NavLink, PageTree


class NavigationTestCase(TestCase):
    def test_instance(self):
        instance = Navigation.objects.create().initialize_from_form(NavigationForm)
        self.assertEqual(str(instance), "Navigation (1)")
        self.assertEqual(instance.get_short_description(), "(light)")


class PageTreeTestCase(TestCase):
    def test_instance(self):
        instance = PageTree.objects.create().initialize_from_form(PageTreeForm)
        self.assertEqual(str(instance), "PageTree (1)")
        self.assertEqual(instance.get_short_description(), "")


class NavLinkTestCase(TestCase):
    def test_instance(self):
        instance = NavLink.objects.create().initialize_from_form(NavLinkForm)
        self.assertEqual(str(instance), "NavLink (1)")
        self.assertEqual(instance.get_short_description(), "<link is missing>")
