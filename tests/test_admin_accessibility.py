from types import SimpleNamespace

from django import forms
from django.contrib.admin.helpers import AdminForm
from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.test import SimpleTestCase

from djangocms_frontend.fields import ButtonGroup, ColoredButtonGroup, IconGroup, IconMultiselect


class AdminAccessibilityTests(SimpleTestCase):
    def test_choice_widgets_keep_native_inputs_and_icon_names(self):
        for widget_class in (ButtonGroup, ColoredButtonGroup, IconGroup, IconMultiselect):
            with self.subTest(widget=widget_class.__name__):
                widget = widget_class(choices=[("start", "Align start"), ("end", "Align end")])
                html = widget.render("alignment", "start", attrs={"id": "id_alignment"})
                self.assertNotIn("display: none", html)
                self.assertIn('for="id_alignment_0"', html)
                self.assertIn('id="id_alignment_0"', html)
                self.assertIn("Align start", html)
                if widget_class in (IconGroup, IconMultiselect):
                    self.assertIn('class="frontend-sr-only">Align start</span>', html)
                    self.assertIn('aria-hidden="true"', html)

    def test_tabs_have_panel_relationships_and_text_indicators(self):
        html = render_tab_fixture()
        self.assertIn('aria-label="Plugin settings"', html)
        self.assertIn('aria-controls="tab-1"', html)
        self.assertIn('aria-labelledby="lnk-1"', html)
        self.assertIn('type="button" role="tab"', html)
        self.assertIn("Contains errors", html)
        self.assertIn("Has custom attributes", html)
        self.assertNotIn('data-bs-toggle="tab"', html)


def render_tab_fixture():
    class Form(forms.Form):
        title = forms.CharField()
        attributes = forms.CharField()

    form = Form(data={"title": "Example", "attributes": ""})
    adminform = AdminForm(
        form,
        [
            ("Main", {"fields": ["title"]}),
            ("Attributes", {"fields": ["attributes"], "classes": ["collapse", "attributes"]}),
        ],
        {},
    )
    # Render the project's blocks without the CMS admin shell or database context.
    template = get_template("djangocms_frontend/admin/base-tabs.html").template
    block = next(node for node in template.nodelist.get_nodes_by_type(BlockNode) if node.name == "field_sets")
    context = Context(
        {
            "adminform": adminform,
            "original": SimpleNamespace(pk=1, attributes={"class": "example"}),
        }
    )
    with context.bind_template(template):
        return block.render(context)
