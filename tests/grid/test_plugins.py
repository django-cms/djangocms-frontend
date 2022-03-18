import warnings

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.grid.cms_plugins import (
    GridColumnPlugin,
    GridContainerPlugin,
    GridRowPlugin,
)
from djangocms_frontend.contrib.grid.forms import (
    GridColumnForm,
    GridContainerForm,
    GridRowForm,
)

from ..fixtures import DJANGO_CMS4, TestFixture


class GridPluginTestCase(TestFixture, CMSTestCase):
    def test_container_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=GridContainerPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(GridContainerForm)
        plugin.save()
        self.assertEqual(
            plugin.plugin_type,
            "GridContainerPlugin",
        )

    def test_grid_row_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=GridRowPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(GridRowForm)
        plugin.save()
        self.assertEqual(
            plugin.plugin_type,
            "GridRowPlugin",
        )

    def test_grid_column_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=GridColumnPlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(GridColumnForm)
        plugin.save()
        self.assertEqual(
            plugin.plugin_type,
            "GridColumnPlugin",
        )

    def test_plugin_structure(self):
        container = add_plugin(
            placeholder=self.placeholder,
            plugin_type=GridContainerPlugin.__name__,
            language=self.language,
            config=dict(background_shadow="reg"),
        )
        container.initialize_from_form(GridContainerForm)
        container.save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shadow")

        row = add_plugin(
            target=container,
            placeholder=self.placeholder,
            plugin_type=GridRowPlugin.__name__,
            language=self.language,
        )
        row.initialize_from_form(GridRowForm)
        row.save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="row">')

        # add column with values
        plugin = add_plugin(
            target=row,
            placeholder=self.placeholder,
            plugin_type=GridColumnPlugin.__name__,
            language=self.language,
            config=dict(xs_col=12),
        )
        plugin.initialize_from_form(GridColumnForm).save()

        self.publish(self.page, self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('<div class="col col-12">' in response.content.decode("utf-8"))
            or ('<div class="col-12 col">' in response.content.decode("utf-8")),
            f'<div class="col col-12"> not found in {response.content.decode("utf-8")}',
        )

        # add row without values
        add_plugin(
            target=row,
            placeholder=self.placeholder,
            plugin_type=GridColumnPlugin.__name__,
            language=self.language,
        ).initialize_from_form(GridColumnForm).save()

        self.publish(self.page, self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="col">')

    def test_row_plugin_creation(self):
        data = {
            "create": 5,
            "tag_type": "div",
            "margin_devices": ["xs"],
            "padding_devices": ["xl"],
        }

        form = GridRowForm(
            {"config": {"a": 1}, **data}
        )  # GridRowForm & GridColumnForm need config explicitly not empty
        self.assertTrue(form.is_valid())

        if (
            not DJANGO_CMS4
        ):  # TODO: Test for django CMS 4 (failing due to rights issue?)
            request_url = self.get_add_plugin_uri(
                placeholder=self.placeholder,
                plugin_type=GridRowPlugin.__name__,
                language=self.language,
            )
            # create 5 column plugins

            with self.login_user_context(self.superuser), warnings.catch_warnings():
                # hide the "DontUsePageAttributeWarning" warning when using
                # `get_add_plugin_uri` to get cleaner test results
                warnings.simplefilter("ignore")
                response = self.client.post(request_url, data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<div class="success">')
