import inspect

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.frontend_forms import cms_plugins
from djangocms_frontend.contrib.frontend_forms.cms_plugins.form_plugins import (
    FormElementPlugin,
)

from ..fixtures import TestFixture


class FormEditorTestCase(TestFixture, CMSTestCase):
    def test_form_editor(self):
        form = add_plugin(
            placeholder=self.placeholder,
            plugin_type=cms_plugins.FormPlugin.__name__,
            language=self.language,
            config=dict(
                form_selection="",
                form_name="my-test-form",
            ),
        )
        form.initialize_from_form()

        for item, cls in cms_plugins.__dict__.items():
            if inspect.isclass(cls) and issubclass(cls, FormElementPlugin):
                field = add_plugin(
                    placeholder=self.placeholder,
                    plugin_type=cls.__name__,
                    target=form,
                    language=self.language,
                    config=dict(
                        field_name="field_" + item,
                    ),
                )
                field.initialize_from_form()

        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/@dcf-frontend_forms/1"')
        self.assertContains(response, '<input type="hidden" name="csrfmiddlewaretoken"')
        for item, cls in cms_plugins.__dict__.items():
            if inspect.isclass(cls) and issubclass(cls, FormElementPlugin):
                self.assertContains(response, f'name="field_{item}"')
