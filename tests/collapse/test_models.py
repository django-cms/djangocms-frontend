from django.test import TestCase

from djangocms_frontend.contrib.collapse.models import (
    Collapse,
    CollapseContainer,
    CollapseTrigger,
)


class B5CollapseModelTestCase(TestCase):
    def test_collapse_instance(self):
        instance = Collapse.objects.create()
        self.assertEqual(str(instance), "Collapse (1)")
        self.assertEqual(instance.get_short_description(), "(collapse-1)")

    def test_collapse_trigger_instance(self):
        instance = CollapseTrigger.objects.create(
            config={"trigger_identifier": "Monty Python"}
        )
        self.assertEqual(str(instance), "CollapseTrigger (1)")
        self.assertEqual(instance.get_short_description(), "(Monty Python)")

    def test_collapse_container_instance(self):
        instance = CollapseContainer.objects.create(
            config={"container_identifier": "Monty Python"}
        )
        self.assertEqual(str(instance), "CollapseContainer (1)")
        self.assertEqual(instance.get_short_description(), "(Monty Python)")
