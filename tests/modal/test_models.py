from django.test import TestCase

from djangocms_frontend.contrib.modal.models import Modal, ModalTrigger, ModalContainer, ModalInner


class ModalModelTestCase(TestCase):
    def test_Modal_instance(self):
        instance = Modal.objects.create()
        self.assertEqual(str(instance), "Modal (1)")
        self.assertEqual(instance.get_short_description(), "(modal-1)")

    def test_modal_trigger_instance(self):
        instance = ModalTrigger.objects.create(
            config={"trigger_identifier": "Monty Python"}
        )
        self.assertEqual(str(instance), "ModalTrigger (1)")
        self.assertEqual(instance.get_short_description(), "(Monty Python)")

    def test_modal_container_instance(self):
        instance = ModalContainer.objects.create(
            config={"container_identifier": "Monty Python"}
        )
        self.assertEqual(str(instance), "ModalContainer (1)")
        self.assertEqual(instance.get_short_description(), "(Monty Python)")

    def test_modal_inner_instance(self):
        instance = ModalInner.objects.create(
            config={"container_identifier": "Monty Python"}
        )
        self.assertEqual(str(instance), "ModalInner (1)")
        self.assertEqual(instance.get_short_description(), "(Monty Python)")
