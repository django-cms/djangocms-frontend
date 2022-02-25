from django.test import TestCase

from djangocms_frontend.contrib.tabs.models import Tab, TabItem


class TabsModelTestCase(TestCase):
    def test_tab_instance(self):
        instance = Tab.objects.create(
            config=dict(tab_type="nav-tabs", tab_alignment="")
        )
        self.assertEqual(str(instance), "Tab (1)")
        self.assertEqual(instance.get_short_description(), "(nav-tabs)")
        instance.config["tab_alignment"] = "nav-fill"
        self.assertEqual(instance.get_short_description(), "(nav-tabs) .nav-fill")

    def test_tab_item_instance(self):
        instance = TabItem.objects.create(config=dict(tab_title=""))
        self.assertEqual(str(instance), "TabItem (1)")
        self.assertEqual(instance.get_short_description(), "")
