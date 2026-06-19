from unittest import mock

from cms.test_utils.testcases import CMSTestCase
from django import forms
from django.template import TemplateDoesNotExist
from django.test import SimpleTestCase

from djangocms_frontend import component_base
from djangocms_frontend.component_base import (
    CMSFrontendComponent,
    _component_qualname_parts,
    _insert_template_folder,
)
from tests.fixtures import TestFixture


class _FakeInstance:
    """Minimal stand-in for a plugin model instance (carries ``config`` and an
    optional ``parent`` whose ``get_plugin_instance`` returns itself)."""

    def __init__(self, template=None, parent=None):
        self.config = {"template": template} if template else {}
        self.parent = parent

    def get_plugin_instance(self):
        return (self, None)


class _FakePlugin:
    """Stands in for the plugin the component's ``get_render_template`` is
    attached to - it only needs a ``render_template``."""

    get_render_template = CMSFrontendComponent.get_render_template

    def __init__(self, render_template):
        self.render_template = render_template


class ComponentNestingTestCase(SimpleTestCase):
    """Unit tests for the ``ComponentMeta`` nesting wiring."""

    def test_nested_component_is_qualified(self):
        class Tab(CMSFrontendComponent):
            class Meta:
                name = "Tabs"
                render_template = "tabs/content.html"

            class Item(CMSFrontendComponent):
                class Meta:
                    name = "Tab item"
                    render_template = "tabs/item.html"

        # Parent keeps its name, child is qualified: Tab.Item -> TabItem.
        self.assertEqual(Tab.__name__, "Tab")
        self.assertEqual(Tab.Item.__name__, "TabItem")

    def test_nested_relationship_is_wired_up(self):
        class Tab(CMSFrontendComponent):
            class Meta:
                name = "Tabs"
                render_template = "tabs/content.html"

            class Item(CMSFrontendComponent):
                class Meta:
                    name = "Tab item"
                    render_template = "tabs/item.html"

        self.assertEqual(Tab.Item.Meta.parent_classes, ["TabPlugin"])
        self.assertTrue(Tab.Item.Meta.require_parent)
        self.assertTrue(Tab.Meta.allow_children)
        self.assertEqual([c.__name__ for c in Tab._nested_components], ["TabItem"])

    def test_explicit_meta_overrides_nesting_defaults(self):
        class Box(CMSFrontendComponent):
            class Meta:
                name = "Box"
                render_template = "box.html"

            class Item(CMSFrontendComponent):
                class Meta:
                    name = "Item"
                    render_template = "item.html"
                    parent_classes = ["SomethingElsePlugin"]
                    require_parent = False

        self.assertEqual(Box.Item.Meta.parent_classes, ["SomethingElsePlugin"])
        self.assertFalse(Box.Item.Meta.require_parent)

    def test_deep_nesting_qualifies_names_and_parents(self):
        class Tab(CMSFrontendComponent):
            class Meta:
                name = "T"
                render_template = "t.html"

            class Item(CMSFrontendComponent):
                class Meta:
                    name = "I"
                    render_template = "i.html"

                class Action(CMSFrontendComponent):
                    class Meta:
                        name = "A"
                        render_template = "a.html"

        self.assertEqual(Tab.Item.__name__, "TabItem")
        self.assertEqual(Tab.Item.Action.__name__, "TabItemAction")
        self.assertEqual(Tab.Item.Action.Meta.parent_classes, ["TabItemPlugin"])
        self.assertEqual([c.__name__ for c in Tab.Item._nested_components], ["TabItemAction"])

    def test_top_level_component_is_not_nested(self):
        class Plain(CMSFrontendComponent):
            class Meta:
                name = "Plain"
                render_template = "plain.html"

        self.assertEqual(Plain.__name__, "Plain")
        self.assertFalse(hasattr(Plain.Meta, "parent_classes"))
        self.assertEqual(Plain._nested_components, [])

    def test_component_qualname_parts(self):
        self.assertEqual(_component_qualname_parts("Tab"), ["Tab"])
        self.assertEqual(_component_qualname_parts("Tab.Item"), ["Tab", "Item"])
        # Function-local definitions ignore the enclosing scope.
        self.assertEqual(_component_qualname_parts("mod.fn.<locals>.Tab.Item"), ["Tab", "Item"])


class ChildClassesAutoTestCase(SimpleTestCase):
    """Unit tests for ``_get_child_classes`` across django CMS versions."""

    def _nested_parent(self):
        class Tab(CMSFrontendComponent):
            class Meta:
                name = "Tabs"
                render_template = "tabs/content.html"

            class Item(CMSFrontendComponent):
                class Meta:
                    name = "Tab item"
                    render_template = "tabs/item.html"

        return Tab

    def test_nested_parent_uses_auto_on_cms_51(self):
        Tab = self._nested_parent()
        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", True):
            self.assertEqual(Tab._get_child_classes({}), "auto")

    def test_nested_parent_enumerates_before_cms_51(self):
        Tab = self._nested_parent()
        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", False):
            self.assertEqual(Tab._get_child_classes({}), ["TabItemPlugin"])

    def test_slots_use_auto_on_cms_51(self):
        class Hero(CMSFrontendComponent):
            class Meta:
                name = "Hero"
                render_template = "hero.html"
                slots = (("title", "Title"),)

        slots = Hero.get_slot_plugins()
        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", True):
            self.assertEqual(Hero._get_child_classes(slots), "auto")
        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", False):
            self.assertEqual(Hero._get_child_classes(slots), ["HeroTitlePlugin"])

    def test_plain_allow_children_stays_unrestricted(self):
        class Box(CMSFrontendComponent):
            class Meta:
                name = "Box"
                render_template = "box.html"
                allow_children = True

        # No nested components and no slots: ``None`` (django CMS reads that as
        # "unrestricted"; an explicit ``[]`` would instead mean "no children").
        for flag in (True, False):
            with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", flag):
                self.assertIsNone(Box._get_child_classes({}))

    def test_explicit_empty_child_classes_means_no_children(self):
        class Box(CMSFrontendComponent):
            class Meta:
                name = "Box"
                render_template = "box.html"
                allow_children = True
                child_classes = []  # explicit: no children allowed

        for flag in (True, False):
            with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", flag):
                self.assertEqual(Box._get_child_classes({}), [])

    def test_explicit_child_classes_respected_and_extended_with_slots(self):
        class Box(CMSFrontendComponent):
            class Meta:
                name = "Box"
                render_template = "box.html"
                child_classes = ["FooPlugin"]
                slots = (("title", "Title"),)

        slots = Box.get_slot_plugins()
        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", True):
            self.assertEqual(Box._get_child_classes(slots), ["FooPlugin", "BoxTitlePlugin"])

    def test_explicit_auto_is_respected_on_old_cms(self):
        class Box(CMSFrontendComponent):
            class Meta:
                name = "Box"
                render_template = "box.html"
                child_classes = "auto"

        with mock.patch.object(component_base, "_CMS_AUTO_CHILD_CLASSES", False):
            self.assertEqual(Box._get_child_classes({}), "auto")


class GetRenderTemplateTestCase(SimpleTestCase):
    """Unit tests for the default ``get_render_template`` resolution."""

    def test_inserts_template_folder_before_file_name(self):
        plugin = _FakePlugin("tabs/content.html")
        instance = _FakeInstance(template="pills")
        with mock.patch.object(component_base, "select_template") as select:
            result = plugin.get_render_template({}, instance, None)
        self.assertEqual(result, "tabs/pills/content.html")
        select.assert_called_once_with(["tabs/pills/content.html"])

    def test_falls_back_to_bare_template_when_missing(self):
        plugin = _FakePlugin("tabs/content.html")
        instance = _FakeInstance(template="ghost")
        with mock.patch.object(component_base, "select_template", side_effect=TemplateDoesNotExist("x")):
            result = plugin.get_render_template({}, instance, None)
        self.assertEqual(result, "tabs/content.html")

    def test_returns_bare_template_without_selection(self):
        plugin = _FakePlugin("tabs/content.html")
        instance = _FakeInstance(template=None)
        with mock.patch.object(component_base, "select_template") as select:
            result = plugin.get_render_template({}, instance, None)
        self.assertEqual(result, "tabs/content.html")
        select.assert_not_called()

    def test_child_inherits_parent_template(self):
        parent = _FakeInstance(template="pills")
        child = _FakeInstance(template=None, parent=parent)
        plugin = _FakePlugin("tabs/item.html")
        with mock.patch.object(component_base, "select_template") as select:
            result = plugin.get_render_template({}, child, None)
        self.assertEqual(result, "tabs/pills/item.html")
        select.assert_called_once_with(["tabs/pills/item.html"])

    def test_insert_template_folder_helper(self):
        self.assertEqual(_insert_template_folder("tabs/content.html", "pills"), "tabs/pills/content.html")
        self.assertEqual(_insert_template_folder("content.html", "pills"), "pills/content.html")


class NestedComponentRegistrationTestCase(TestFixture, CMSTestCase):
    """Integration test: a nested component registers as a child plugin."""

    def test_nested_component_is_registered_as_child_plugin(self):
        from cms.plugin_pool import plugin_pool

        from djangocms_frontend.component_base import _CMS_AUTO_CHILD_CLASSES

        self.assertIn("TabComponentPlugin", plugin_pool.plugins)
        self.assertIn("TabComponentItemPlugin", plugin_pool.plugins)

        parent = plugin_pool.get_plugin("TabComponentPlugin")
        child = plugin_pool.get_plugin("TabComponentItemPlugin")

        self.assertTrue(parent.allow_children)
        self.assertEqual(child.parent_classes, ["TabComponentPlugin"])
        self.assertTrue(child.require_parent)

        expected = "auto" if _CMS_AUTO_CHILD_CLASSES else ["TabComponentItemPlugin"]
        self.assertEqual(parent.child_classes, expected)
