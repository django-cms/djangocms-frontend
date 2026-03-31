import json
import unittest
import uuid

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.models import Site
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm
from djangocms_frontend.contrib.alert.models import Alert
from djangocms_frontend.templatetags.frontend import (
    get_attributes,
    is_registering_component,
    json_dumps,
    set_html_id,
    update_component_properties,
)

from .fixtures import DJANGO_CMS4, TestFixture


class GetAttributesTagTestCase(TestCase):
    """Tests for the get_attributes simple tag."""

    def test_basic_attributes(self):
        result = get_attributes({"data-toggle": "modal", "id": "test"})
        self.assertIn('data-toggle="modal"', result)
        self.assertIn('id="test"', result)

    def test_class_merging(self):
        result = get_attributes({"class": "existing"}, "extra-class")
        self.assertIn("existing", result)
        self.assertIn("extra-class", result)

    def test_classes_without_attribute_field(self):
        result = get_attributes(None, "my-class another-class")
        self.assertIn("my-class", result)
        self.assertIn("another-class", result)

    def test_empty_attribute_field_with_classes(self):
        result = get_attributes({}, "my-class")
        self.assertIn('class="my-class"', result)

    def test_boolean_attribute(self):
        """Attributes with empty/None value render without =value."""
        result = get_attributes({"disabled": ""})
        self.assertIn("disabled", result)
        self.assertNotIn("=", result)

    def test_none_returns_empty(self):
        result = get_attributes(None)
        self.assertEqual(result, "")

    def test_escapes_values(self):
        result = get_attributes({"data-val": '<script>alert("xss")</script>'})
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_multiple_add_classes(self):
        result = get_attributes(None, "class-a", "class-b class-c")
        self.assertIn("class-a", result)
        self.assertIn("class-b", result)
        self.assertIn("class-c", result)


class SetHtmlIdTagTestCase(TestCase):
    """Tests for the set_html_id simple tag."""

    def test_assigns_counter_based_id_with_request(self):
        factory = RequestFactory()
        request = factory.get("/")
        context = Context({"request": request})

        instance = Alert.objects.create()
        result = set_html_id(context, instance)
        self.assertEqual(result, "frontend-plugins-1")
        self.assertEqual(instance.html_id, "frontend-plugins-1")

    def test_increments_counter(self):
        factory = RequestFactory()
        request = factory.get("/")
        context = Context({"request": request})

        instance1 = Alert.objects.create()
        instance2 = Alert.objects.create()
        set_html_id(context, instance1)
        set_html_id(context, instance2)
        self.assertEqual(instance1.html_id, "frontend-plugins-1")
        self.assertEqual(instance2.html_id, "frontend-plugins-2")

    def test_uses_uuid_without_request(self):
        context = Context({})
        instance = Alert.objects.create()
        result = set_html_id(context, instance)
        self.assertTrue(result.startswith("uuid4-"))

    def test_returns_existing_id(self):
        """If html_id is already set, don't reassign."""
        factory = RequestFactory()
        request = factory.get("/")
        context = Context({"request": request})

        instance = Alert.objects.create()
        instance.html_id = "custom-id"
        result = set_html_id(context, instance)
        self.assertEqual(result, "custom-id")


class JsonDumpsFilterTestCase(TestCase):
    """Tests for the json_dumps filter."""

    def test_basic_dict(self):
        result = json_dumps({"key": "value"})
        self.assertEqual(json.loads(result), {"key": "value"})

    def test_with_lazy_translation(self):
        from django.utils.translation import gettext_lazy

        data = {"label": gettext_lazy("Hello")}
        result = json_dumps(data)
        parsed = json.loads(result)
        self.assertEqual(parsed["label"], "Hello")

    def test_list(self):
        result = json_dumps([1, 2, 3])
        self.assertEqual(json.loads(result), [1, 2, 3])


class HtmlSafeFilterTestCase(TestCase):
    """Tests for the html_safe filter."""

    def test_returns_string(self):
        from djangocms_frontend.templatetags.frontend import html_safe

        result = html_safe("<b>bold</b>")
        self.assertIn("bold", str(result))


class SafeCaptionFilterTestCase(TestCase):
    """Tests for the safe_caption filter."""

    def test_strips_wrapping_p_tags(self):
        from djangocms_frontend.templatetags.frontend import safe_caption

        result = safe_caption("<p>Hello World</p>")
        self.assertNotIn("<p>", str(result))
        self.assertIn("Hello World", str(result))

    def test_preserves_nested_p_tags(self):
        from djangocms_frontend.templatetags.frontend import safe_caption

        result = safe_caption("<p>Para 1</p><p>Para 2</p>")
        # Should not strip because there are nested p tags
        self.assertIn("<p>", str(result))

    def test_non_p_wrapped_content(self):
        from djangocms_frontend.templatetags.frontend import safe_caption

        result = safe_caption("<div>Content</div>")
        self.assertIn("<div>", str(result))


class GetRelatedObjectFilterTestCase(TestCase):
    """Tests for the get_related_object filter."""

    def test_valid_reference(self):
        from djangocms_frontend.templatetags.frontend import get_related_object

        site = Site.objects.get_current()
        reference = {"model": "sites.site", "pk": site.pk}
        result = get_related_object(reference)
        self.assertEqual(result, site)

    def test_invalid_reference(self):
        from djangocms_frontend.templatetags.frontend import get_related_object

        reference = {"model": "sites.site", "pk": -9999}
        result = get_related_object(reference)
        self.assertIsNone(result)


class IsRegisteringComponentTestCase(TestCase):
    """Tests for the is_registering_component helper."""

    def test_returns_false_without_cms_components(self):
        context = Context({})
        self.assertFalse(is_registering_component(context))

    def test_returns_false_without_cms_component_key(self):
        context = Context({"_cms_components": {}})
        self.assertFalse(is_registering_component(context))

    def test_returns_true_when_registering(self):
        context = Context({"_cms_components": {"cms_component": [((), {})]}})
        self.assertTrue(is_registering_component(context))

    def test_returns_false_when_multiple_components(self):
        context = Context({"_cms_components": {"cms_component": [((), {}), ((), {})]}})
        self.assertFalse(is_registering_component(context))


class UpdateComponentPropertiesTestCase(TestCase):
    """Tests for update_component_properties helper."""

    def test_set_property(self):
        context = Context({"_cms_components": {"cms_component": [((), {})]}})
        update_component_properties(context, "allow_children", True)
        _, kwargs = context["_cms_components"]["cms_component"][0]
        self.assertTrue(kwargs["allow_children"])

    def test_append_property(self):
        context = Context({"_cms_components": {"cms_component": [((), {})]}})
        update_component_properties(context, "slots", ("SlotPlugin", "Title"), append=True)
        update_component_properties(context, "slots", ("SlotPlugin2", "Body"), append=True)
        _, kwargs = context["_cms_components"]["cms_component"][0]
        self.assertEqual(len(kwargs["slots"]), 2)


class InlineFieldTestCase(TestFixture, CMSTestCase):
    """Tests for the inline_field template tag."""

    @unittest.skipUnless(DJANGO_CMS4, "django CMS 4+ required")
    def test_check_source_called_exactly_once(self):
        """Regression test: placeholder.check_source must be called exactly once
        when rendering inline_field, not once per tag evaluation."""
        from unittest.mock import MagicMock, patch

        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(AlertForm).save()

        factory = RequestFactory()
        request = factory.get("/")
        request.user = self.superuser
        request.session = SessionStore()
        request.session["inline_editing"] = True

        tpl = Template('{% load frontend %}{% inline_field instance "alert_context" %}')

        with patch.object(type(self.placeholder), "check_source", return_value=True) as mock_check:
            tpl.render(Context({"request": request, "instance": parent}))

        mock_check.assert_called_once_with(self.superuser)


class ChildPluginsRenderTestCase(TestFixture, CMSTestCase):
    """End-to-end test for childplugins rendering."""

    def test_alert_renders_child_plugins(self):
        from djangocms_frontend.contrib.badge.cms_plugins import BadgePlugin
        from djangocms_frontend.contrib.badge.forms import BadgeForm

        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=AlertPlugin.__name__,
            language=self.language,
        )
        parent.initialize_from_form(AlertForm).save()

        child = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=BadgePlugin.__name__,
            language=self.language,
            config=dict(badge_text="TestBadge"),
        )
        child.initialize_from_form(BadgeForm).save()
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestBadge")
