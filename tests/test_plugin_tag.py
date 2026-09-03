import warnings

from cms.test_utils.testcases import CMSTestCase
from django.contrib.sites.shortcuts import get_current_site
from django.template import engines
from django.test import override_settings

from tests.fixtures import TestFixture
from tests.helpers import get_filer_image

django_engine = engines["django"]


@override_settings(DEBUG=True)
class PluginTagTestCase(TestFixture, CMSTestCase):
    def test_tag_default_rendering(self):
        template = django_engine.from_string("""
        {% load frontend cms_tags %}
        {% plugin "alert" %}Alert{% endplugin %}
        """)

        result = template.render({"request": None})

        self.assertInHTML('<div class="alert-primary alert" role="alert"><div>Alert</div></div>', result)

    def test_tag_rendering_with_paramter(self):
        template = django_engine.from_string("""
        {% load frontend cms_tags %}
        {% plugin "alert" alert_context="secondary" alert_dismissible=True %}Alert{% endplugin %}
        """)
        expected_result = """<div class="alert alert-secondary alert-dismissible" role="alert">
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button><div>Alert
        </div></div>"""

        result = template.render({"request": None})

        self.assertInHTML(expected_result, result)

    def test_simple_tag(self):
        template = django_engine.from_string("""
        {% load frontend  %}
        {% plugin "badge" badge_text="My badge" badge_context="info" badge_pills=False %}
           This content is ignored.
        {% endplugin %}""")
        expected_result = """<span class="badge bg-info">My badge</span>"""

        result = template.render({"request": None})

        self.assertInHTML(expected_result, result)

    def test_complex_tags(self):
        from djangocms_frontend.plugin_tag import plugin_tag_pool

        template = django_engine.from_string("""{% load frontend %}
        {% plugin "card" card_alignment="center" card_outline="info" card_text_color="primary" card_full_height=True %}
            {% plugin "cardinner" inner_type="card-header" text_alignment="start" %}
                <h4>Card title</h4>
            {% endplugin %}
            {% plugin "cardinner" inner_type="card-body" text_alignment="center" %}
                Some quick example text to build on the card title and make up the
                bulk of the card's content.
            {% endplugin %}
            {% plugin "listgroupitem" %}An item{% endplugin %}
            {% plugin "listgroupitem" %}A second item{% endplugin %}
            {% plugin "listgroupitem" %}A third item{% endplugin %}
        {% endplugin %}""")

        expected_result = """
        <div class="card text-primary text-center border-info h-100">
            <div class="text-start card-header"><h4>Card title</h4></div>
            <div class="card-body text-center">
                Some quick example text to build on the card title and make up the
                bulk of the card's content.
            </div>
            <div class="list-group-item">An item</div>
            <div class="list-group-item">A second item</div>
            <div class="list-group-item">A third item</div>
        </div>"""

        result = template.render({"request": None})

        self.assertIn("cardinner", plugin_tag_pool)

        self.assertInHTML(expected_result, result)

    def test_link_plugin(self):
        if hasattr(self, "create_url"):
            grouper = self.create_url(manual_url="/test/").url_grouper
            template = django_engine.from_string("""{% load frontend %}
            {% plugin "textlink" name="Click" url_grouper=grouper site=test_site link_type="btn" link_context="primary" link_outline=False %}
                Click me!
            {% endplugin %}
        """)  # noqa: B950,E501
        else:
            grouper = None
            template = django_engine.from_string("""{% load frontend djangocms_link_tags %}{{ "test"|to_link }}
                {% plugin "textlink" name="Click" link="/test/"|to_link link_type="btn" link_context="primary" link_outline=False %}
                    Click me!
                {% endplugin %}
            """)  # noqa: B950,E501

        expected_result = """<a href="/test/" class="btn btn-primary">Click me!</a>"""

        result = template.render({"request": None, "test_site": get_current_site(None), "grouper": grouper})
        self.assertInHTML(expected_result, result)

    @override_settings(DEBUG=True)
    def test_non_existing_plugin(self):
        template = django_engine.from_string("""{% load frontend %}
            {% plugin "nonexisting" %}
                This should not be rendered.
            {% endplugin %}
        """)
        expected_result = (
            '<!-- To use "nonexisting" with the {% plugin %} template tag, add its plugin class to the '
            "CMS_COMPONENT_PLUGINS setting -->"
        )

        result = template.render({"request": None})

        self.assertEqual(expected_result.strip(), result.strip())

    def test_non_frontend_plugin(self):
        template = django_engine.from_string("""{% load frontend %}
            {% plugin "text" body="<p>my text</p>" %}
                This should not be rendered.
            {% endplugin %}
        """)
        expected_result = "<p>my text</p>"

        result = template.render({"request": None})

        self.assertInHTML(expected_result, result)

    def test_kwargs_do_not_leak_between_plugin_calls(self):
        """Regression test: kwargs from one {% plugin %} call must not
        bleed into subsequent calls of the same plugin type."""
        template = django_engine.from_string("""{% load frontend %}
        {% plugin "alert" alert_context="warning" %}First{% endplugin %}
        {% plugin "alert" %}Second{% endplugin %}
        """)

        result = template.render({"request": None})

        # The second alert should use the default context ("primary"), not "warning"
        self.assertIn("alert-warning", result)
        self.assertIn("alert-primary", result)

    def test_autohero_component_registered_for_plugin_tag(self):
        from cms.plugin_pool import plugin_pool

        from djangocms_frontend.plugin_tag import plugin_tag_pool

        # Check that the AutoHero plugin is registered
        self.assertIn("AutoHeroPlugin", plugin_pool.plugins)

        # Check for the AutoHero plugin registration in the plugin_tag_pool
        self.assertIn("autohero", plugin_tag_pool)

    @override_settings(
        DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES=(
            ("default", "Default"),
            ("custom", "Custom"),
        )
    )
    def test_plugin_tag_uses_dynamic_carousel_slide_templates(self):
        from cms.api import add_plugin

        from djangocms_frontend.contrib.carousel.cms_plugins import CarouselPlugin
        from djangocms_frontend.contrib.carousel.forms import CarouselForm

        parent_custom = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
            config={"template": "custom"},
        )
        parent_custom.initialize_from_form(CarouselForm).save()

        parent_default = add_plugin(
            placeholder=self.placeholder,
            plugin_type=CarouselPlugin.__name__,
            language=self.language,
            config={"template": "default"},
        )
        parent_default.initialize_from_form(CarouselForm).save()

        image = get_filer_image()
        try:
            template = django_engine.from_string("""
            {% load frontend cms_tags %}
            {% plugin "carouselslide" parent=parent_custom carousel_image=image position=0 %}
                <p>Custom slide content</p>
            {% endplugin %}
            {% plugin "carouselslide" parent=parent_default carousel_image=image position=0 %}
                <p>Default slide content</p>
            {% endplugin %}
            """)

            result = template.render(
                {
                    "request": None,
                    "image": image,
                    "parent_custom": parent_custom,
                    "parent_default": parent_default,
                }
            )

            # Custom slide template in tests is intentionally empty.
            self.assertNotIn("Custom slide content", result)
            self.assertIn("Default slide content", result)
        finally:
            image.delete()

    def test_plugin_tag_silent_during_component_registration(self):
        """Component templates are rendered at startup to collect their declarations. At that point
        the plugin tag pool is still empty, so a {% plugin %} tag in a component template must not
        warn about a missing CMS_COMPONENT_PLUGINS entry. Declarations nested in its block still
        need to be picked up."""
        from collections import defaultdict

        from django import forms
        from sekizai.context import SekizaiContext

        template = django_engine.from_string("""{% load frontend cms_component %}
            {% cms_component "ComponentUsingPluginTag" %}
            {% plugin "nonexisting" %}
                {% field "title" forms.CharField %}
            {% endplugin %}
        """)
        # Same context as used by CMSAutoComponentDiscovery
        context = SekizaiContext({"_cms_components": defaultdict(list), "forms": forms, "instance": {}})

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = template.template.render(context)

        self.assertEqual([str(warning.message) for warning in caught], [])
        self.assertEqual(result.strip(), "")
        self.assertEqual([field[0][0] for field in context["_cms_components"]["fields"]], ["title"])

    # Plugin names given as dotted path are imported directly, so nothing in this setting makes the
    # plugin pool discover plugins on its own.
    @override_settings(CMS_COMPONENT_PLUGINS=["djangocms_frontend.cms_plugins.CMSUIPlugin"])
    def test_setup_discovers_plugins(self):
        """setup() runs in AppConfig.ready() and must trigger plugin discovery itself. Relying on
        another app to have done so (django.contrib.admin's autodiscover) only works if that app is
        listed before djangocms_frontend in INSTALLED_APPS."""
        from unittest.mock import patch

        from cms.plugin_pool import plugin_pool

        from djangocms_frontend import plugin_tag

        original_pool = dict(plugin_tag.plugin_tag_pool)
        try:
            plugin_tag.plugin_tag_pool.clear()
            with patch.object(plugin_pool, "discover_plugins", wraps=plugin_pool.discover_plugins) as discover:
                plugin_tag.setup()
            rebuilt_pool = dict(plugin_tag.plugin_tag_pool)
        finally:
            plugin_tag.plugin_tag_pool.clear()
            plugin_tag.plugin_tag_pool.update(original_pool)

        discover.assert_called_once()
        self.assertIn("card", rebuilt_pool)
        self.assertIn("gridcontainer", rebuilt_pool)

    def test_setup_with_djangocms_frontend_as_first_installed_app(self):
        """djangocms_frontend must build a complete plugin tag pool no matter where it is listed in
        INSTALLED_APPS. Needs a fresh interpreter, as both app loading and plugin discovery only
        happen once per process."""
        import pathlib
        import subprocess
        import sys

        import tests

        script = """
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")
import tests.test_settings as test_settings

# Worst case: no app that triggers plugin discovery is loaded before djangocms_frontend, and
# CMS_COMPONENT_PLUGINS only holds dotted paths, which are imported without touching the pool.
test_settings.CMS_COMPONENT_PLUGINS = ["djangocms_frontend.cms_plugins.CMSUIPlugin"]
installed_apps = [app for app in test_settings.INSTALLED_APPS if app != "djangocms_frontend"]
test_settings.INSTALLED_APPS = ["djangocms_frontend", *installed_apps]

import django
django.setup()

from djangocms_frontend.plugin_tag import plugin_tag_pool
print(",".join(sorted(plugin_tag_pool)))
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            cwd=str(pathlib.Path(tests.__file__).parent.parent),
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        tag_names = result.stdout.strip().split(",")
        self.assertIn("card", tag_names)
        self.assertIn("gridcontainer", tag_names)
