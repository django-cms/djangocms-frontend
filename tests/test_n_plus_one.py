from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext

from djangocms_frontend.contrib.alert.cms_plugins import AlertPlugin
from djangocms_frontend.contrib.alert.forms import AlertForm
from djangocms_frontend.contrib.tabs.cms_plugins import TabItemPlugin, TabPlugin
from djangocms_frontend.contrib.tabs.forms import TabForm, TabItemForm

from .fixtures import TestFixture


class NPlusOneTestCase(TestFixture, CMSTestCase):
    """Frontend plugins must render with a query count that is independent of
    the number of plugins on the page. A growing query count would indicate an
    N+1 problem where each plugin triggers its own database query at render time.
    """

    def _add_alerts(self, count):
        for _ in range(count):
            plugin = add_plugin(
                placeholder=self.placeholder,
                plugin_type=AlertPlugin.__name__,
                language=self.language,
            )
            plugin.initialize_from_form(AlertForm).save()

    def _add_tab_with_items(self, count):
        """Adds a Tab plugin with ``count`` TabItem children, each containing an
        Alert. ``TabItemPlugin.get_render_template`` reads ``instance.parent``,
        which is a prime candidate for an N+1 query at render time.
        """
        tab = add_plugin(
            placeholder=self.placeholder,
            plugin_type=TabPlugin.__name__,
            language=self.language,
        )
        tab.initialize_from_form(TabForm).save()
        for _ in range(count):
            item = add_plugin(
                placeholder=self.placeholder,
                plugin_type=TabItemPlugin.__name__,
                language=self.language,
                target=tab,
            )
            item.initialize_from_form(TabItemForm).save()
            alert = add_plugin(
                placeholder=self.placeholder,
                plugin_type=AlertPlugin.__name__,
                language=self.language,
                target=item,
            )
            alert.initialize_from_form(AlertForm).save()

    def _render_query_count(self):
        self.publish(self.page, self.language)
        # Prime caches (content types, permissions, ...) so the measured render
        # only reflects the queries needed to render the placeholder's plugins.
        with self.login_user_context(self.superuser):
            self.client.get(self.request_url)
            with CaptureQueriesContext(connection) as ctx:
                response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        return len(ctx.captured_queries)

    def test_rendering_plugins_does_not_create_n_plus_one(self):
        # Baseline: render the page with a small number of plugins.
        self._add_alerts(3)
        baseline = self._render_query_count()

        # Add many more plugins of the same type to the same placeholder.
        self._add_alerts(30)
        scaled = self._render_query_count()

        # Rendering 11x as many plugins must not increase the number of queries.
        # If it does, plugins are being fetched one-by-one (an N+1 problem).
        self.assertEqual(
            scaled,
            baseline,
            f"Rendering 33 plugins issued {scaled} queries but 3 plugins only "
            f"issued {baseline}. Frontend plugins create an N+1 query problem "
            "when rendering.",
        )

    def test_nested_plugins_do_not_create_n_plus_one(self):
        # Baseline: a Tab with 3 TabItems, each holding an Alert.
        self._add_tab_with_items(3)
        baseline = self._render_query_count()

        # Scale up the number of tab items (and their nested alerts).
        self._add_tab_with_items(30)
        scaled = self._render_query_count()

        # TabItem renders by reading ``instance.parent``. If the parent (or its
        # downcast instance) is fetched per item, the query count grows with the
        # number of items — an N+1 problem.
        self.assertEqual(
            scaled,
            baseline,
            f"Rendering the larger tab issued {scaled} queries but the small "
            f"tab only issued {baseline}. Nested frontend plugins create an "
            "N+1 query problem when rendering.",
        )
