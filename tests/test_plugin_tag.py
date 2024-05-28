from cms.test_utils.testcases import CMSTestCase
from django.template import engines

from tests.fixtures import TestFixture

django_engine = engines["django"]


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
        expected_result = """<div class="alert alert-secondary alert-dismissible alert-primary" role="alert">
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
            <div class="card-body text-start text-center card-header">
                Some quick example text to build on the card title and make up the
                bulk of the card's content.
            </div>
            <div class="list-group-item">An item</div>
            <div class="list-group-item">A second item</div>
            <div class="list-group-item">A third item</div>
        </div>"""
        result = template.render({"request": None})

        self.assertInHTML(expected_result, result)

    def test_link_component(self):
        template = django_engine.from_string("""{% load frontend %}
            {% plugin "link" name="Click" external_link="/" link_type="btn" link_context="primary" link_outline=False %}
                Click me!
            {% endplugin %}
        """)

        expected_result = """<a href="/" class="btn btn-primary">Click me!</a>"""

        result = template.render({"request": None})

        self.assertInHTML(expected_result, result)
