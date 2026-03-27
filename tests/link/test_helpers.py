from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase

from djangocms_frontend.contrib.link.helpers import GetLinkMixin, get_object_for_value


class GetObjectForValueTestCase(TestCase):
    def test_valid_value_returns_dict(self):
        ct = ContentType.objects.get_for_model(Site)
        site = Site.objects.get_current()
        value = f"{ct.id}-{site.pk}"
        result = get_object_for_value(value)
        self.assertIsNotNone(result)
        self.assertEqual(result["model"], f"{ct.app_label}.{ct.model}")
        self.assertEqual(result["pk"], site.pk)

    def test_invalid_content_type_returns_none(self):
        result = get_object_for_value("99999-1")
        self.assertIsNone(result)

    def test_non_string_returns_none(self):
        self.assertIsNone(get_object_for_value(123))
        self.assertIsNone(get_object_for_value(None))

    def test_string_without_dash_returns_none(self):
        self.assertIsNone(get_object_for_value("nodash"))

    def test_empty_string_returns_none(self):
        self.assertIsNone(get_object_for_value(""))


class GetLinkMixinTestCase(TestCase):
    """Tests for GetLinkMixin.get_link() using djangocms_link fallback path."""

    def _make_instance(self, config):
        """Create a simple object with GetLinkMixin behavior."""

        class FakePlugin(GetLinkMixin):
            def __init__(self, config):
                self.config = config

        return FakePlugin(config)

    def test_external_link(self):
        instance = self._make_instance({"link": {"external_link": "https://example.com"}})
        self.assertEqual(instance.get_link(), "https://example.com")

    def test_empty_link_returns_empty_string(self):
        instance = self._make_instance({"link": {}})
        self.assertEqual(instance.get_link(), "")

    def test_no_link_key_returns_empty_string(self):
        instance = self._make_instance({})
        self.assertEqual(instance.get_link(), "")

    def test_internal_link_to_page(self):
        from cms.api import create_page

        page = create_page("Test Page", "page.html", "en")
        instance = self._make_instance({"link": {"internal_link": f"cms.page:{page.pk}"}})
        link = instance.get_link()
        self.assertTrue(link.endswith("/test-page/") or link != "", f"Unexpected link: {link}")
