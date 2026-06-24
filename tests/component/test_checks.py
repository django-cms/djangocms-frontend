from django import forms
from django.test import SimpleTestCase

from djangocms_frontend.apps import check_component_plugin_behavior
from djangocms_frontend.component_base import CMSFrontendComponent
from djangocms_frontend.component_pool import components
from djangocms_frontend.ui_plugin_base import CMSUIComponent


class PluginMixinTestCase(SimpleTestCase):
    """The nested ``PluginMixin`` is mixed into the plugin's bases."""

    def test_plugin_mixin_sits_before_base_in_mro(self):
        class WithMixin(CMSFrontendComponent):
            __module__ = "tests.test_app.cms_components"

            class Meta:
                name = "WithMixinComponent"
                render_template = "x.html"

            title = forms.CharField()

            class PluginMixin:
                def get_render_template(self, context, instance, placeholder):
                    return "custom.html"

        plugin = WithMixin.plugin_factory()
        mro = plugin.__mro__

        self.assertIn(WithMixin.PluginMixin, mro)
        # Before CMSUIComponent, so ``super()`` reaches the component defaults.
        self.assertLess(mro.index(WithMixin.PluginMixin), mro.index(CMSUIComponent))
        self.assertEqual(plugin().get_render_template({}, None, None), "custom.html")

    def test_no_plugin_mixin_uses_base_defaults(self):
        class Plain(CMSFrontendComponent):
            __module__ = "tests.test_app.cms_components"

            class Meta:
                name = "PlainComponent"
                render_template = "x.html"

            title = forms.CharField()

        plugin = Plain.plugin_factory()
        # The slot-creating default lives on CMSUIComponent and is inherited.
        self.assertIs(plugin.save_model, CMSUIComponent.save_model)


class DeprecatedPluginBehaviorCheckTestCase(SimpleTestCase):
    """``check_component_plugin_behavior`` reports legacy top-level declarations."""

    def test_attrs_declared_on_component_are_detected(self):
        class OldStyle(CMSFrontendComponent):
            __module__ = "tests.test_app.cms_components"

            class Meta:
                name = "OldStyleComponent"
                render_template = "x.html"

            title = forms.CharField()
            TEMPLATES = (("z", "Z"),)

            def save_model(self, request, obj, form, change):
                pass

        # Reported in declaration order, ``get_render_template`` is absent here.
        self.assertEqual(OldStyle._deprecated_plugin_attrs(), ["save_model", "TEMPLATES"])

        # The factory still grafts them for backwards compatibility.
        plugin = OldStyle.plugin_factory()
        self.assertIn("save_model", plugin.__dict__)
        self.assertEqual(plugin.__dict__["TEMPLATES"], (("z", "Z"),))

        components._components["OldStyleComponent"] = OldStyle
        try:
            warnings = check_component_plugin_behavior()
        finally:
            components._components.pop("OldStyleComponent", None)

        match = [w for w in warnings if w.obj.endswith("OldStyle")]
        self.assertEqual(len(match), 1)
        self.assertEqual(match[0].id, "djangocms_frontend.W003")

    def test_plugin_mixin_is_not_flagged(self):
        class Clean(CMSFrontendComponent):
            __module__ = "tests.test_app.cms_components"

            class Meta:
                name = "CleanComponent"
                render_template = "x.html"

            title = forms.CharField()

            class PluginMixin:
                def save_model(self, request, obj, form, change):
                    super().save_model(request, obj, form, change)

        self.assertEqual(Clean._deprecated_plugin_attrs(), [])
