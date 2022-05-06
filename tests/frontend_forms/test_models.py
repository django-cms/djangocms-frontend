from django.test import TestCase

from djangocms_frontend.contrib.frontend_forms.forms import FormsForm
from djangocms_frontend.contrib.frontend_forms.models import Form, FormEntry


class FormsModelTestCase(TestCase):
    def test_form_instance(self):
        instance = Form.objects.create()
        instance.initialize_from_form(FormsForm)
        self.assertEqual(str(instance), "Form (1)")
        self.assertEqual(instance.get_short_description(), "<unnamed>")
        instance.config["form_name"] = "my-test-form"
        self.assertEqual(instance.get_short_description(), "(my-test-form)")

        entry = FormEntry.objects.create(form_name=instance.form_name)
        self.assertEqual(str(entry), "my-test-form (1)")
