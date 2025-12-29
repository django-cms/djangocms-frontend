from unittest.mock import patch

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.template import Context

from djangocms_frontend.contrib.collapse.cms_plugins import (
    CollapseContainerPlugin,
    CollapsePlugin,
    CollapseTriggerPlugin,
)
from djangocms_frontend.contrib.collapse.forms import (
    CollapseContainerForm,
    CollapseForm,
    CollapseTriggerForm,
)
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.templatetags.frontend import set_html_id

from ..fixtures import TestFixture


class CollapsePluginTestCase(TestFixture, CMSTestCase):
    def test_collapse_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapsePlugin.__name__,
            language=self.language,
        )
        plugin.initialize_from_form(CollapseForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-bs-children=".card"')
        self.assertContains(response, 'role="tablist"')

    def test_collapse_trigger_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapseTriggerPlugin.__name__,
            language=self.language,
            config=dict(
                trigger_identifier=10,
            ),
        )
        plugin.initialize_from_form(CollapseTriggerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-controls="10"')
        self.assertContains(response, 'data-bs-target="#10"')
        self.assertContains(response, 'id="trigger-10"')

    def test_collapse_container_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CollapsePlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(CollapseForm).save()

        plugin = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=CollapseContainerPlugin.__name__,
            language=self.language,
            config=dict(
                container_identifier=10,
            ),
        )
        plugin.initialize_from_form(CollapseContainerForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-labelledby="trigger-10"')
        self.assertContains(response, "10")

    def test_collapse_html_id(self):
        def create_plugin():
            plugin = add_plugin(
                placeholder=self.placeholder,
                plugin_type=CollapsePlugin.__name__,
                language=self.language,
            )
            plugin.initialize_from_form(CollapseForm).save()
            self.publish(self.page, self.language)

        create_plugin()
        create_plugin()
        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            """<div id="collapse-frontend-plugins-1" data-bs-children=".card" role="tablist"></div>""",
            html=True,
        )
        self.assertContains(
            response,
            """<div id="collapse-frontend-plugins-2" data-bs-children=".card" role="tablist"></div>""",
            html=True,
        )

    def test_set_html_id(self):
        instance = FrontendUIItem()
        context = Context()
        with patch("os.urandom", lambda n: b"\x1bB\x96\xabyI\xf6`\xd0\xc0,\xf8\x83\xe8,\xb8"):
            html_id = set_html_id(context, instance)
        identifier = "uuid4-1b4296ab-7949-4660-90c0-2cf883e82cb8"
        self.assertEqual(html_id, identifier)
        self.assertEqual(instance.html_id, identifier)
