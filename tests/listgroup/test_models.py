from django.test import TestCase

from djangocms_frontend.contrib.listgroup.forms import ListGroupForm, ListGroupItemForm
from djangocms_frontend.contrib.listgroup.models import ListGroup, ListGroupItem


class ListGroupModelTestCase(TestCase):
    def test_list_group_instance(self):
        instance = ListGroup.objects.create().initialize_from_form(ListGroupForm)
        self.assertEqual(str(instance), "ListGroup (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.list_group_flush = True
        self.assertEqual(instance.get_short_description(), ".list-group-flush")

    def test_list_group_item_instance(self):
        instance = ListGroupItem.objects.create().initialize_from_form(
            ListGroupItemForm
        )
        self.assertEqual(str(instance), "ListGroupItem (1)")
        self.assertEqual(instance.get_short_description(), "")
        instance.list_context = "primary"
        self.assertEqual(instance.get_short_description(), ".list-group-item-primary")
        instance.list_state = "active"
        self.assertEqual(
            instance.get_short_description(), ".list-group-item-primary .active"
        )
