import re

from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from .fixtures import TestFixture

# Identical configuration for both the contrib and the component tab trees.
PARENT_CONFIG = dict(
    template="default",
    tab_type="nav-tabs",
    tab_alignment="",
    tab_index=1,
    tab_effect="fade",
    attributes={},
)
ITEM_CONFIGS = [
    dict(tab_title="First tab", tab_bordered=True, attributes={}),
    dict(tab_title="Second tab", tab_bordered=False, attributes={}),
]


def _normalize(html):
    """Drop the only tree-specific difference: the auto-generated plugin pks
    embedded in the tab element ids."""
    html = re.sub(r"tab-label-\d+", "tab-label-PK", html)
    html = re.sub(r"tab-\d+", "tab-PK", html)
    return html.strip()


class TabsByteIdenticalTestCase(TestFixture, CMSTestCase):
    """The Tabs example component renders byte-identically to contrib.tabs."""

    def _build_tabs(self, placeholder, parent_type, item_type):
        parent = add_plugin(
            placeholder=placeholder,
            plugin_type=parent_type,
            language=self.language,
            config=dict(PARENT_CONFIG),
        )
        for item_config in ITEM_CONFIGS:
            add_plugin(
                target=parent,
                placeholder=placeholder,
                plugin_type=item_type,
                language=self.language,
                config=dict(item_config),
            )
        return parent

    def _render_current(self):
        self.publish(self.page, self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        return response.content.decode("utf-8")

    def test_renders_byte_identical_to_contrib(self):
        from cms.models import CMSPlugin

        # Render contrib tabs, then the example tabs into the same placeholder.
        self._build_tabs(self.placeholder, "TabPlugin", "TabItemPlugin")
        contrib_html = self._render_current()

        CMSPlugin.objects.filter(placeholder=self.placeholder).delete()
        self._build_tabs(self.placeholder, "TabsPlugin", "TabsItemPlugin")
        example_html = self._render_current()

        self.assertEqual(_normalize(example_html), _normalize(contrib_html))
        # Sanity: the comparison is non-trivial (real tab markup was rendered).
        self.assertIn("tab-pane", _normalize(contrib_html))
        self.assertIn('<ul class="nav nav-tabs', _normalize(contrib_html))


class DoublyNestedComponentTestCase(TestFixture, CMSTestCase):
    """Section > Row > Col: double nesting wires up and renders."""

    def test_registration_and_wiring(self):
        from cms.plugin_pool import plugin_pool

        for name in ("SectionPlugin", "SectionRowPlugin", "SectionRowColPlugin"):
            self.assertIn(name, plugin_pool.plugins)

        section = plugin_pool.get_plugin("SectionPlugin")
        row = plugin_pool.get_plugin("SectionRowPlugin")
        col = plugin_pool.get_plugin("SectionRowColPlugin")

        self.assertTrue(section.allow_children)
        self.assertEqual(row.parent_classes, ["SectionPlugin"])
        self.assertTrue(row.require_parent)
        self.assertEqual(col.parent_classes, ["SectionRowPlugin"])
        self.assertTrue(col.require_parent)
        self.assertTrue(col.allow_children)

    def test_renders_nested_structure(self):
        section = add_plugin(placeholder=self.placeholder, plugin_type="SectionPlugin", language=self.language)
        row = add_plugin(
            target=section, placeholder=self.placeholder, plugin_type="SectionRowPlugin", language=self.language
        )
        add_plugin(target=row, placeholder=self.placeholder, plugin_type="SectionRowColPlugin", language=self.language)
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("<section", body)
        self.assertIn('<div class="row"', body)
        self.assertIn('<div class="col"', body)
