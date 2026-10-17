from copy import deepcopy
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.http import QueryDict
from django.template import Context, Template
from django.test import SimpleTestCase, TestCase

from djangocms_frontend import tokens
from djangocms_frontend.common.bootstrap5.responsive import get_display_classes
from djangocms_frontend.common.bootstrap5.spacing import get_spacing_classes
from djangocms_frontend.contrib.grid.forms import GridContainerForm, GridRowForm
from djangocms_frontend.contrib.grid.frameworks.bootstrap5 import get_grid_values, get_row_cols_grid_values
from djangocms_frontend.contrib.link.forms import LinkForm
from djangocms_frontend.frameworks import bootstrap5_tokens as adapter
from djangocms_frontend.models import FrontendUIItem


class UniversalTokenTests(SimpleTestCase):
    def test_spacing_has_physical_meaning_and_preserves_legacy_values(self):
        legacy = {"margin_x": "mx-3", "padding_y": "pt-4", "space_size": "5", "gutters": "2"}
        canonical = tokens.normalize_config(legacy)
        self.assertEqual(canonical["margin_x"], {"property": "margin", "side": "horizontal", "size": "rem-1"})
        self.assertEqual(canonical["padding_y"]["size"], "rem-1.5")
        self.assertEqual(canonical["space_size"], "rem-3")
        self.assertEqual(adapter.config_values(canonical) | {tokens.VERSION_KEY: 1}, legacy | {tokens.VERSION_KEY: 1})
        self.assertEqual(legacy["margin_x"], "mx-3")
        self.assertEqual(tokens.normalize_config(canonical), canonical)

    def test_mappings_are_role_specific_and_leave_extension_json_alone(self):
        extension = {"size": "3", "class": "btn-sm", "xxl_col": 8}
        original = {
            "attributes": extension,
            "link_type": "btn",
            "link_size": "btn-sm",
            "size_x": "50",
            "size_y": "min-vh-100",
            "background_context": "light",
            "navbar_design": "dark",
            "background_shadow": "reg",
            "inner_type": "card-body",
            "tab_type": "nav-tabs",
        }
        result = tokens.normalize_config(original)
        self.assertEqual(result["link_type"], "button")
        self.assertEqual(result["link_size"], "sm")
        self.assertEqual(result["size_x"], "percent-50")
        self.assertEqual(result["size_y"], "min-viewport")
        self.assertEqual(result["background_context"], "neutral-light")
        self.assertEqual(result["navbar_design"], "dark")
        self.assertIs(result["attributes"], extension)
        self.assertFalse(tokens.config_issues(result))
        self.assertEqual(adapter.config_values(result), original | {tokens.VERSION_KEY: 1})

    def test_breakpoint_fields_and_lists(self):
        original = {
            "xxl_col": 6,
            "xxl_offset": 2,
            "row_cols_xxl": 3,
            "margin_devices": ["xs", "xxl"],
            "responsive_visibility": ["xxl"],
            "navbar_breakpoint": "xxl",
        }
        result = tokens.normalize_config(original)
        self.assertEqual(result["2xl_col"], 6)
        self.assertEqual(result["row_cols_2xl"], 3)
        self.assertEqual(result["margin_devices"], ["xs", "2xl"])
        self.assertEqual(adapter.config_values(result), original | {tokens.VERSION_KEY: 1})
        instance = SimpleNamespace(config=result)
        self.assertEqual(get_grid_values(instance), ["col-xxl-6", "offset-xxl-2"])
        self.assertEqual(get_row_cols_grid_values(instance), ["row-cols-xxl-3"])
        self.assertEqual(get_display_classes(["2xl"]), get_display_classes(["xxl"]))

    def test_conflicting_keys_and_future_versions_are_rejected(self):
        for config in ({"xxl_col": 3, "2xl_col": 4}, {tokens.VERSION_KEY: 2}, []):
            with self.subTest(config=config), self.assertRaises(ValueError):
                tokens.normalize_config(config)
        self.assertEqual(tokens.normalize_config({"xxl_col": 4, "2xl_col": 4})["2xl_col"], 4)

    def test_responsive_spacing_reset_preserves_output(self):
        canonical = tokens.normalize_value("margin_x", "mx-3")
        expected = ["mx-md-3", "mx-xl-0"]
        self.assertEqual(get_spacing_classes([canonical], ["md", "lg"]), expected)
        self.assertEqual(get_spacing_classes([canonical], ["2xl"]), ["mx-xxl-3"])

    def test_strict_adapter_and_class_enumeration(self):
        self.assertEqual(adapter.utility_classes("padding-top", "rem-1", breakpoint="md"), ("pt-md-3",))
        self.assertEqual(
            adapter.component_classes("button", color="danger", variant="outline", size="sm"),
            ("btn", "btn-outline-danger", "btn-sm"),
        )
        for args in (("padding-top", "rem-0.75"), ("foreground", "accent")):
            with self.subTest(args=args), self.assertRaises(ValueError):
                adapter.utility_classes(*args)
        self.assertNotIn("accent", adapter.supported_options("button")["colors"])
        self.assertIn("pt-md-3", set(adapter.iter_class_names()))
        self.assertIn("btn-outline-danger", set(adapter.iter_class_names()))
        self.assertIs(adapter.utility_classes("padding-top", "rem-1"), adapter.utility_classes("padding-top", "rem-1"))

    def test_opacity_preserves_exact_percentages(self):
        for percent in (10, 25, 50, 75, 100):
            self.assertEqual(
                tokens.normalize_config({"background_opacity": str(percent)})["background_opacity"], percent
            )
        self.assertTrue(tokens.config_issues({"background_opacity": 150}))

    def test_unknown_values_reported_without_erasing_content(self):
        result = tokens.normalize_config({"space_size": "custom", "margin_x": "mz-3", "other": "untouched"})
        self.assertEqual(result["margin_x"], "mz-3")
        self.assertEqual(len(tokens.config_issues(result)), 2)
        self.assertEqual(result["other"], "untouched")

    def test_template_filter_projects_class_values(self):
        instance = FrontendUIItem(config={"tab_type": "tabs", "tab_alignment": "vertical"})
        template = Template(
            '{% load frontend_tokens %}{{ instance|framework_value:"tab_type" }} {{ instance|framework_value:"tab_alignment" }}'
        )
        self.assertEqual(template.render(Context({"instance": instance})), "nav-tabs flex-column")


class UniversalFormTests(TestCase):
    def test_canonical_and_legacy_form_input_write_canonical_config(self):
        for value in ("bounded", "container"):
            form = GridContainerForm(
                data={"container_type": value, "tag_type": "div", "margin_devices": ["xl"], "padding_devices": ["xs"]}
            )
            self.assertTrue(form.is_valid(), form.errors)
            self.assertEqual(form.instance.config["container_type"], "bounded")
            self.assertEqual(form.instance.config[tokens.VERSION_KEY], 1)

    def test_editing_migrated_record_replaces_alias_without_conflict(self):
        original = tokens.normalize_config(
            {"row_cols_xxl": 3, "margin_devices": ["xl"], "padding_devices": ["xs"], "extension": {"x": 1}}
        )
        instance = FrontendUIItem(config=deepcopy(original))
        form = GridRowForm(
            instance=instance, data={"row_cols_xxl": 5, "margin_devices": ["xl"], "padding_devices": ["xs"]}
        )
        self.assertEqual(form.initial["row_cols_xxl"], 3)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.config["row_cols_2xl"], 5)
        self.assertNotIn("row_cols_xxl", form.instance.config)
        self.assertEqual(form.instance.config["extension"], {"x": 1})
        self.assertEqual(original["row_cols_2xl"], 3)

    def test_unchanged_native_choice_retains_original_universal_colour_role(self):
        instance = FrontendUIItem(config=tokens.normalize_config({"background_context": "inverse"}))
        form = GridContainerForm(
            instance=instance,
            data={
                "container_type": "container",
                "tag_type": "div",
                "background_context": "dark",
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
            },
        )
        self.assertEqual(form.initial["background_context"], "dark")
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.config["background_context"], "inverse")

    def test_querydict_preserves_multiple_devices(self):
        data = QueryDict("container_type=bounded&tag_type=div&margin_devices=xs&margin_devices=2xl&padding_devices=xs")
        form = GridContainerForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.config["margin_devices"], ["xs", "2xl"])

    def test_structured_spacing_form_input_and_existing_initials(self):
        spacing = {"property": "margin", "side": "horizontal", "size": "rem-1"}
        form = GridContainerForm(
            data={
                "container_type": "bounded",
                "tag_type": "div",
                "margin_x": spacing,
                "margin_devices": ["md"],
                "padding_devices": ["xs"],
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.config["margin_x"], spacing)
        unbound = GridContainerForm(instance=form.instance)
        self.assertEqual(unbound.initial["margin_x"], "mx-3")

    def test_invalid_original_schema_cannot_be_overwritten_by_form(self):
        for config in ({tokens.VERSION_KEY: 2},):
            with self.subTest(config=config):
                instance = FrontendUIItem(config=deepcopy(config))
                form = GridRowForm(instance=instance, data={"margin_devices": ["xs"], "padding_devices": ["xs"]})
                self.assertFalse(form.is_valid())
                self.assertEqual(instance.config, config)

    def test_editable_conflicting_grid_keys_can_be_repaired(self):
        instance = FrontendUIItem(config={"row_cols_xxl": 3, "row_cols_2xl": 5})
        form = GridRowForm(
            instance=instance,
            data={
                "row_cols_xxl": 4,
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
            },
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], 4)
        self.assertNotIn("row_cols_xxl", form.cleaned_data["config"])

    def test_uneditable_conflicting_grid_keys_resolve_to_canonical(self):
        config = {"row_cols_xxl": 3, "row_cols_2xl": 5}
        instance = FrontendUIItem(config=deepcopy(config))
        form = GridContainerForm(
            instance=instance,
            data={
                "container_type": "container",
                "tag_type": "div",
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
            },
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], 5)
        self.assertNotIn("row_cols_xxl", form.cleaned_data["config"])

    def test_reinitializing_canonical_defaults_keeps_existing_grid_values(self):
        instance = FrontendUIItem(config=tokens.normalize_config({"row_cols_xxl": 4}))
        instance.initialize_from_form(GridRowForm)
        self.assertEqual(instance.config["row_cols_2xl"], 4)
        self.assertNotIn("row_cols_xxl", instance.config)

    def test_unsupported_token_input_is_a_form_error(self):
        form = GridContainerForm(
            data={
                "container_type": "bounded",
                "tag_type": "div",
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
                "padding_x": {"property": "padding", "side": "horizontal", "size": "rem-0.75"},
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Unsupported native Bootstrap 5 spacing", str(form.errors))
        self.assertIn("padding_x", form.errors)
        self.assertFalse(form.non_field_errors())

    def test_link_form_writes_canonical_values(self):
        form = LinkForm(
            data={
                "link_0": "external_link",
                "link_1": "https://example.com",
                "link_type": "button",
                "link_size": "sm",
                "template": "default",
                "margin_devices": ["xs"],
                "padding_devices": ["xs"],
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.config["link_type"], "button")
        self.assertEqual(form.instance.config["link_size"], "sm")

    def test_plugin_tag_breakpoint_overrides_canonical_defaults(self):
        for field in ("xxl_col", "2xl_col"):
            with self.subTest(field=field):
                template = Template(
                    '{% load frontend %}{% plugin "gridcolumn" ' + field + "=6 %}Column{% endplugin %}"
                )
                result = template.render(Context({"request": None}))
                self.assertIn("col-xxl-6", result)

    def test_token_rendering_does_not_query_database(self):
        instance = FrontendUIItem(config=tokens.normalize_config({"xxl_col": 6, "row_cols_xxl": 3}))
        with self.assertNumQueries(0):
            get_grid_values(instance)
            get_row_cols_grid_values(instance)
            adapter.component_classes("button", color="danger")


class UniversalMigrationTests(TestCase):
    def make_item(self, config):
        return FrontendUIItem.objects.create(config=config, plugin_type="GridRowPlugin", language="en")

    def run_command(self, *args):
        stdout, stderr = StringIO(), StringIO()
        call_command(
            "frontend", "migrate", "--from", "bootstrap5", "--to", "universal", *args, stdout=stdout, stderr=stderr
        )
        return stdout.getvalue(), stderr.getvalue()

    def test_dry_run_apply_and_repeat(self):
        item = self.make_item({"margin_x": "mx-3", "xxl_col": 6, "attributes": {"class": "project-class"}})
        output, errors = self.run_command("--dry-run")
        self.assertIn("Would migrate 1", output)
        self.assertEqual(errors, "")
        item.refresh_from_db()
        self.assertEqual(item.config["margin_x"], "mx-3")
        self.run_command()
        item.refresh_from_db()
        self.assertEqual(item.config["2xl_col"], 6)
        self.assertEqual(item.config["margin_x"]["size"], "rem-1")
        self.assertEqual(item.config["attributes"]["class"], "project-class")
        output, _ = self.run_command()
        self.assertIn("Migrated 0 configurations; 1 unchanged", output)

    def test_unmapped_records_are_reported_and_left_untouched(self):
        item = self.make_item({"space_size": "project-size"})
        output, errors = self.run_command()
        self.assertIn("1 skipped", output)
        self.assertIn(f"pk={item.pk}", errors)
        item.refresh_from_db()
        self.assertEqual(item.config, {"space_size": "project-size"})

    def test_fail_on_unmapped_rolls_back_previous_changes(self):
        good = self.make_item({"gutters": "3"})
        self.make_item({"space_size": "project-size"})
        with self.assertRaises(CommandError):
            self.run_command("--fail-on-unmapped")
        good.refresh_from_db()
        self.assertEqual(good.config, {"gutters": "3"})

    def test_version_and_conflict_are_reported_without_changes(self):
        self.make_item({tokens.VERSION_KEY: 2})
        self.make_item({"xxl_col": 3, "2xl_col": 4})
        output, errors = self.run_command()
        self.assertIn("2 skipped", output)
        self.assertIn("Unsupported universal token schema version", errors)
        self.assertIn("Conflicting legacy and canonical", errors)

    def test_concurrent_change_aborts_conversion(self):
        item = self.make_item({"gutters": "3"})
        with patch("django.db.models.query.QuerySet.update", return_value=0):
            with self.assertRaisesMessage(CommandError, "changed concurrently"):
                self.run_command()
        item.refresh_from_db()
        self.assertEqual(item.config, {"gutters": "3"})

    def test_requires_both_source_and_target(self):
        with self.assertRaises(CommandError):
            call_command("frontend", "migrate", "--from", "bootstrap5")


class Bootstrap5RenderParityTests(SimpleTestCase):
    def test_migrated_plugins_emit_identical_classes_and_attributes(self):
        from importlib import import_module

        class Terminal:
            def render(self, context, instance, placeholder):
                return context

        cases = (
            (
                "common.bootstrap5.background",
                "BackgroundMixin",
                {"background_context": "light", "background_shadow": "reg", "background_opacity": "75"},
            ),
            ("common.bootstrap5.sizing", "SizingMixin", {"size_x": "50", "size_y": "min-vh-100"}),
            (
                "common.bootstrap5.spacing",
                "SpacingMixin",
                {"margin_x": "mx-3", "padding_y": "pt-4", "margin_devices": ["md", "lg"], "padding_devices": ["xxl"]},
            ),
            ("common.bootstrap5.responsive", "ResponsiveMixin", {"responsive_visibility": ["xs", "xxl"]}),
            ("contrib.grid.frameworks.bootstrap5", "GridContainerRenderMixin", {"container_type": "container-fluid"}),
            (
                "contrib.grid.frameworks.bootstrap5",
                "GridRowRenderMixin",
                {
                    "vertical_alignment": "align-items-center",
                    "horizontal_alignment": "justify-content-between",
                    "gutters": "3",
                    "row_cols_xxl": 2,
                },
            ),
            (
                "contrib.grid.frameworks.bootstrap5",
                "GridColumnRenderMixin",
                {"text_alignment": "center", "column_alignment": "align-self-end", "xxl_col": 6, "xxl_ms": True},
            ),
            (
                "contrib.card.frameworks.bootstrap5",
                "CardRenderMixin",
                {"card_alignment": "center", "card_outline": "dark", "card_text_color": "light"},
            ),
            ("contrib.card.frameworks.bootstrap5", "CardInnerRenderMixin", {"inner_type": "card-body"}),
            ("contrib.card.frameworks.bootstrap5", "CardLayoutRenderMixin", {"card_type": "row", "row_cols_xxl": 2}),
            ("contrib.tabs.frameworks.bootstrap5", "TabRenderMixin", {"tab_alignment": "flex-column"}),
            (
                "contrib.carousel.frameworks.bootstrap5",
                "CarouselRenderMixin",
                {"carousel_transition": "carousel-fade"},
            ),
            (
                "contrib.navigation.frameworks.bootstrap5",
                "NavigationRenderMixin",
                {"navbar_design": "dark", "navbar_breakpoint": "xxl"},
            ),
            (
                "contrib.link.frameworks.bootstrap5",
                "LinkRenderMixin",
                {"link_type": "btn", "link_context": "dark", "link_size": "btn-sm", "link_outline": True},
            ),
            (
                "contrib.alert.frameworks.bootstrap5",
                "AlertRenderMixin",
                {"alert_context": "light", "alert_shadow": "reg", "alert_dismissible": True},
            ),
            (
                "contrib.badge.frameworks.bootstrap5",
                "BadgeRenderMixin",
                {"badge_context": "dark", "badge_pills": True},
            ),
            ("contrib.icon.frameworks.bootstrap5", "IconRenderMixin", {"icon_foreground": "light"}),
            (
                "contrib.listgroup.frameworks.bootstrap5",
                "ListGroupItemRenderMixin",
                {"list_context": "light", "list_state": "active"},
            ),
            (
                "contrib.utilities.frameworks.bootstrap5",
                "SpacingRenderMixin",
                {"space_property": "m", "space_sides": "x", "space_size": "3", "space_device": "xxl"},
            ),
            (
                "contrib.utilities.frameworks.bootstrap5",
                "HeadingRenderMixin",
                {"heading_context": "dark", "heading_alignment": "center"},
            ),
        )
        for module, name, config in cases:
            with self.subTest(mixin=name):
                mixin = getattr(import_module("djangocms_frontend." + module), name)
                renderer = type("Renderer", (mixin, Terminal), {})()
                original = deepcopy(config)
                legacy = FrontendUIItem(config=deepcopy(config), ui_item="GridRow")
                canonical = FrontendUIItem(config=tokens.normalize_config(config), ui_item="GridRow")
                renderer.render({}, legacy, None)
                renderer.render({}, canonical, None)
                self.assertEqual(set(canonical._additional_classes), set(legacy._additional_classes))
                self.assertEqual(canonical.config, tokens.normalize_config(original))
                self.assertEqual(legacy.config, original)

    def test_tabs_template_keeps_native_classes_after_migration(self):
        from django.template.loader import render_to_string

        config = {"tab_type": "nav-tabs", "tab_alignment": "flex-column"}
        outputs = []
        for data in (config, tokens.normalize_config(config)):
            instance = FrontendUIItem(config=data)
            instance.child_plugin_instances = []
            outputs.append(
                render_to_string("djangocms_frontend/bootstrap5/tabs/default/tabs.html", {"instance": instance})
            )
        self.assertHTMLEqual(*outputs)


class TokenReviewRegressionTests(TestCase):
    def container_data(self, **kwargs):
        return {
            "container_type": "container",
            "tag_type": "div",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **kwargs,
        }

    def test_old_spacing_sides_validate_render_and_migrate(self):
        from djangocms_frontend.contrib.utilities.forms import SpacingForm
        from djangocms_frontend.contrib.utilities.models import Spacing

        for old, canonical, native in (("r", "end", "e"), ("l", "start", "s")):
            with self.subTest(side=old):
                instance = Spacing(
                    config={"space_property": "m", "space_sides": old, "space_size": "3", "space_device": ""}
                )
                form = SpacingForm(instance=instance, data=instance.config)
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.instance.config["space_sides"], canonical)
                self.assertEqual(form.instance.get_base_css_class(), f"m{native}-3")
                self.assertEqual(get_spacing_classes([f"m{old}-3"]), [f"m{native}-3"])
                saved = FrontendUIItem.objects.create(
                    plugin_type="GridRowPlugin", config={"space_property": "m", "space_sides": old, "space_size": "3"}
                )
                call_command("frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=StringIO())
                saved.refresh_from_db()
                self.assertEqual(saved.config["space_sides"], canonical)

    def test_unsupported_token_does_not_crash_plugin_rendering(self):
        for plugin in (
            '{% plugin "alert" alert_shadow="xl" %}Content{% endplugin %}',
            '{% plugin "gridcontainer" background_context="surface-3" %}Content{% endplugin %}',
            '{% plugin "spacing" space_size="rem-0.75" %}{% endplugin %}',
        ):
            with self.subTest(plugin=plugin):
                result = Template("{% load frontend %}" + plugin).render(Context({"request": None}))
                self.assertNotIn("shadow-xl", result)
                self.assertNotIn("bg-surface-3", result)
                self.assertNotIn("rem-0.75", result)
        self.assertEqual(
            get_spacing_classes([{"property": "margin", "side": "all", "size": "rem-0.75"}, "mt-3"]), ["mt-3"]
        )
        template = Template('{% load frontend_tokens %}{{ instance|framework_value:"background_context" }}')
        self.assertEqual(
            template.render(Context({"instance": FrontendUIItem(config={"background_context": "surface-3"})})), ""
        )

    def test_editors_can_replace_a_bad_stored_token(self):
        for replacement in ("primary", ""):
            with self.subTest(replacement=replacement):
                instance = FrontendUIItem(config=tokens.normalize_config({"background_context": "surface-3"}))
                form = GridContainerForm(instance=instance, data=self.container_data(background_context=replacement))
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.instance.config["background_context"], replacement)

    def test_bad_input_is_reported_once_and_bad_initial_can_be_repaired(self):
        # A newly selected unsupported token is an error, reported once.
        other = FrontendUIItem(config=tokens.normalize_config({"background_context": "primary"}))
        form = GridContainerForm(instance=other, data=self.container_data(background_context="surface-3"))
        self.assertFalse(form.is_valid())
        self.assertEqual(str(form.errors["background_context"]).count("Unsupported native Bootstrap 5 value"), 1)
        # The same token posted back unchanged is kept.
        instance = FrontendUIItem(config=tokens.normalize_config({"background_context": "surface-3"}))
        kept = GridContainerForm(instance=instance, data=self.container_data(background_context="surface-3"))
        self.assertTrue(kept.is_valid(), kept.errors)
        self.assertEqual(kept.cleaned_data["config"]["background_context"], "surface-3")
        repaired = GridContainerForm(
            instance=instance,
            initial={"background_context": "surface-3"},
            data=self.container_data(background_context="primary"),
        )
        self.assertTrue(repaired.is_valid(), repaired.errors)

    def test_migration_rejects_other_frameworks_without_writes(self):
        from django.test import override_settings

        item = FrontendUIItem.objects.create(plugin_type="GridRowPlugin", config={"container_type": "container"})
        for framework in ("foundation6", "tailwind"):
            with self.subTest(framework=framework), override_settings(DJANGOCMS_FRONTEND_FRAMEWORK=framework):
                with self.assertRaisesMessage(CommandError, "requires DJANGOCMS_FRONTEND_FRAMEWORK"):
                    call_command("frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=StringIO())
        item.refresh_from_db()
        self.assertEqual(item.config, {"container_type": "container"})

    def test_sqlite_noncanonical_json_formatting_migrates(self):
        from django.db import connection

        if connection.vendor != "sqlite":
            self.skipTest("SQLite text JSON regression")
        item = FrontendUIItem.objects.create(plugin_type="GridRowPlugin", config={})
        table = connection.ops.quote_name(FrontendUIItem._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET config = %s WHERE cmsplugin_ptr_id = %s",
                ['{ "xxl_col" : 6,\n "gutters" : "3" }', item.pk],
            )
        call_command("frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=StringIO())
        item.refresh_from_db()
        self.assertEqual(item.config["gutters"], "rem-1")
        self.assertEqual(item.config["2xl_col"], 6)

    def test_explicit_none_initial_with_and_without_instance(self):
        for instance in (None, FrontendUIItem(config={"container_type": "bounded"})):
            with self.subTest(instance=instance):
                form = GridContainerForm(initial=None, instance=instance, data=self.container_data())
                self.assertTrue(form.is_valid(), form.errors)

    def test_initialization_resolves_conflicts_and_supplies_defaults(self):
        instance = FrontendUIItem(config={"row_cols_xxl": 3, "row_cols_2xl": 5})
        with self.assertLogs("djangocms_frontend.models", "WARNING"):
            instance.initialize_from_form(GridRowForm)
        self.assertNotIn("row_cols_xxl", instance.config)
        self.assertEqual(instance.config["row_cols_2xl"], 5)
        self.assertEqual(instance.config[tokens.VERSION_KEY], 1)
        self.assertIn("gutters", instance.config)
        self.assertEqual(get_row_cols_grid_values(instance), ["row-cols-xxl-5"])
        # The resulting configuration can be edited again.
        form = GridRowForm(instance=instance, data={"margin_devices": ["xs"], "padding_devices": ["xs"]})
        self.assertTrue(form.is_valid(), form.errors)

    def test_structure_board_descriptions_resolve_framework_values(self):
        from djangocms_frontend.contrib.alert.models import Alert
        from djangocms_frontend.contrib.card.models import Card, CardInner, CardLayout
        from djangocms_frontend.contrib.listgroup.models import ListGroupItem
        from djangocms_frontend.contrib.tabs.models import Tab
        from djangocms_frontend.contrib.utilities.models import Spacing

        cases = (
            (Spacing, {"space_property": "m", "space_sides": "", "space_device": "", "space_size": "3"}),
            (Alert, {"alert_context": "dark"}),
            (Card, {"background_context": "dark", "card_outline": "light", "card_alignment": ""}),
            (CardLayout, {"card_type": "row"}),
            (CardInner, {"inner_type": "card-img-overlay"}),
            (Tab, {"tab_type": "nav-tabs", "tab_alignment": "flex-column"}),
            (ListGroupItem, {"list_context": "light", "list_state": "active"}),
        )
        for model, config in cases:
            with self.subTest(model=model.__name__):
                self.assertEqual(
                    model(config=config).get_short_description(),
                    model(config=tokens.normalize_config(config)).get_short_description(),
                )

    def test_framework_filter_delegates_to_adapter(self):
        instance = FrontendUIItem(config={"tab_type": "tabs"})
        with patch.object(adapter, "field_value", return_value="custom-tabs") as resolver:
            result = Template('{% load frontend_tokens %}{{ instance|framework_value:"tab_type" }}').render(
                Context({"instance": instance})
            )
        self.assertEqual(result, "custom-tabs")
        resolver.assert_called_once_with(instance, "tab_type", "")


class TokenSecondReviewTests(TestCase):
    def test_title_only_form_preserves_uneditable_unsupported_value(self):
        from django import forms
        from djangocms_frontend.token_forms import EntangledModelForm

        class TitleOnlyForm(EntangledModelForm):
            title = forms.CharField()

            class Meta:
                model = FrontendUIItem
                entangled_fields = {"config": ["title"]}
                untangled_fields = ()

        original = tokens.normalize_config({"title": "Old", "background_shadow": "xl"})
        instance = FrontendUIItem.objects.create(config=original)
        form = TitleOnlyForm(instance=instance, data={"title": "New"})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        instance.refresh_from_db()
        self.assertEqual(instance.config["title"], "New")
        self.assertEqual(instance.config["background_shadow"], "xl")

    def test_badge_description_matches_legacy_colour(self):
        from djangocms_frontend.contrib.badge.models import Badge

        self.assertEqual(
            Badge(config=tokens.normalize_config({"badge_context": "light"})).get_short_description(), "(light)"
        )

    def test_conflicting_defaults_do_not_crash_initialization(self):
        from djangocms_frontend.contrib.grid.models import GridRow

        defaults = {"row_cols_xxl": 3, "row_cols_2xl": 5}
        for source in ("model", "settings"):
            with self.subTest(source=source):
                with patch.object(GridRow, "default_config", defaults if source == "model" else {}, create=True):
                    with patch(
                        "djangocms_frontend.models.PLUGIN_DEFAULTS",
                        {"GridRow": defaults} if source == "settings" else {},
                    ):
                        with self.assertLogs("djangocms_frontend.models", level="WARNING") as logs:
                            instance = GridRow(config={}).initialize_from_form(GridRowForm)
                        self.assertIn("using row_cols_2xl", logs.output[0])
                self.assertNotIn("row_cols_xxl", instance.config)
                self.assertEqual(instance.config["row_cols_2xl"], 5)
                self.assertEqual(get_row_cols_grid_values(instance), ["row-cols-xxl-5"])
                form = GridRowForm(
                    instance=instance,
                    data={
                        "row_cols_xxl": 4,
                        "margin_devices": ["xs"],
                        "padding_devices": ["xs"],
                    },
                )
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], 4)

    def test_render_errors_honor_the_callers_default(self):
        from djangocms_frontend.contrib.link.frameworks.bootstrap5 import LinkRenderMixin

        class Terminal:
            def render(self, context, instance, placeholder):
                return context

        renderer = type("Renderer", (LinkRenderMixin, Terminal), {})()
        # As before universal tokens: any stored link_type but "link", even an empty
        # or unknown one, renders a button; a missing link_type renders a link.
        for invalid in ({"bad": "type"}, [], "unknown", None, ""):
            with self.subTest(invalid=invalid):
                instance = FrontendUIItem(config={"link_type": invalid, "link_context": "primary"})
                if invalid not in ("", None):  # an empty link_type is a valid button, not an error
                    self.assertEqual(adapter.field_value(instance, "link_type", "link"), "link")
                renderer.render({}, instance, None)
                self.assertIn("btn-primary", instance._additional_classes)
        instance = FrontendUIItem(config={"link_context": "primary"})
        renderer.render({}, instance, None)
        self.assertIn("link-primary", instance._additional_classes)

    def test_badge_and_listgroup_rejected_colours_have_no_broken_classes(self):
        from djangocms_frontend.contrib.badge.frameworks.bootstrap5 import BadgeRenderMixin
        from djangocms_frontend.contrib.listgroup.frameworks.bootstrap5 import ListGroupItemRenderMixin

        class Terminal:
            def render(self, context, instance, placeholder):
                return context

        for mixin, config, expected in (
            (BadgeRenderMixin, {"badge_context": {"bad": 1}, "badge_pills": False}, ["badge"]),
            (ListGroupItemRenderMixin, {"list_context": {"bad": 1}, "list_state": ""}, ["list-group-item"]),
        ):
            with self.subTest(mixin=mixin.__name__):
                instance = FrontendUIItem(config=config)
                type("Renderer", (mixin, Terminal), {})().render({}, instance, None)
                self.assertEqual(instance._additional_classes, expected)

    def test_oracle_path_locks_rows_and_never_compares_lobs(self):
        from django.db import connection
        from django.db.models.query import QuerySet
        from django.test.utils import CaptureQueriesContext

        item = FrontendUIItem.objects.create(plugin_type="GridRowPlugin", config={"gutters": "3"})
        original = QuerySet.select_for_update
        with patch(
            "djangocms_frontend.management.universal_migration.connections",
            {"default": SimpleNamespace(vendor="oracle")},
        ):
            with patch.object(QuerySet, "select_for_update", autospec=True, side_effect=original) as locked:
                with CaptureQueriesContext(connection) as queries:
                    call_command("frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=StringIO())
        self.assertTrue(locked.called)
        updates = [q["sql"] for q in queries if q["sql"].lstrip().upper().startswith("UPDATE")]
        self.assertTrue(updates)
        for query in updates:
            self.assertNotIn("config", query.split("WHERE", 1)[1].lower())
            self.assertNotIn("CAST", query)
        item.refresh_from_db()
        self.assertEqual(item.config["gutters"], "rem-1")

    def test_card_template_wraps_grid_cards_without_render_mixin(self):
        from cms.models import CMSPlugin
        from django.template.loader import render_to_string
        from djangocms_frontend.contrib.card.models import Card, CardLayout

        parent = CMSPlugin(plugin_type="CardLayoutPlugin")
        layout = CardLayout(config=tokens.normalize_config({"card_type": "row"}))
        parent.get_plugin_instance = lambda: (layout, None)
        instance = Card(parent=parent, config={"card_alignment": ""})
        instance.child_plugin_instances = []
        rendered = render_to_string("djangocms_frontend/bootstrap5/card.html", {"instance": instance})
        self.assertIn('<div class="col mb-3">', rendered)

    def test_empty_spacing_is_an_explicit_unset_and_does_not_block_migration(self):
        item = FrontendUIItem.objects.create(
            plugin_type="GridRowPlugin", config={"margin_x": "mx-", "padding_y": "py-", "gutters": "3"}
        )
        self.assertEqual(tokens.normalize_value("margin_x", "mx-"), "")
        self.assertEqual(
            tokens.normalize_value("margin_x", {"property": "margin", "side": "horizontal", "size": ""}), ""
        )
        call_command(
            "frontend", "migrate", "--from", "bootstrap5", "--to", "universal", "--fail-on-unmapped", stdout=StringIO()
        )
        item.refresh_from_db()
        self.assertEqual(item.config["margin_x"], "")
        self.assertEqual(item.config["padding_y"], "")
        self.assertEqual(item.config["gutters"], "rem-1")


class TokenThirdReviewTests(TestCase):
    def test_filter_uses_model_presentation_method(self):
        instance = FrontendUIItem(config={})
        with patch.object(instance, "get_framework_value", return_value="custom") as resolve:
            result = Template('{% load frontend_tokens %}{{ instance|framework_value:"tab_type" }}').render(
                Context({"instance": instance})
            )
        self.assertEqual(result, "custom")
        resolve.assert_called_once_with("tab_type")

    def test_row_creation_writes_canonical_columns(self):
        from cms.models import CMSPlugin
        from unittest.mock import Mock
        from djangocms_frontend.cms_plugins import CMSUIPlugin
        from djangocms_frontend.contrib.grid.cms_plugins import GridRowPlugin

        row = CMSPlugin(position=1, language="en")
        form = SimpleNamespace(cleaned_data={"create": 1, "create_xxl_col": 6})
        with patch.object(CMSUIPlugin, "save_model"):
            with patch("djangocms_frontend.contrib.grid.cms_plugins.add_plugin") as add:
                GridRowPlugin().save_model(Mock(), row, form, False)
        config = add.call_args.args[1].config
        self.assertEqual(config[tokens.VERSION_KEY], 1)
        self.assertEqual(config["2xl_col"], 6)
        self.assertNotIn("xxl_col", config)
        self.assertIn("2xl_ms", config)
        self.assertNotIn("xxl_ml", config)

    def test_card_render_and_template_resolve_parent_once(self):
        from cms.models import CMSPlugin
        from django.template.loader import render_to_string
        from unittest.mock import Mock
        from djangocms_frontend.contrib.card.models import Card, CardLayout
        from djangocms_frontend.contrib.card.frameworks.bootstrap5 import CardRenderMixin

        class Terminal:
            def render(self, context, instance, placeholder):
                return context

        parent = CMSPlugin(plugin_type="CardLayoutPlugin")
        layout = CardLayout(config=tokens.normalize_config({"card_type": "row"}))
        parent.get_plugin_instance = Mock(return_value=(layout, None))
        instance = Card(parent=parent, config={"card_alignment": ""})
        instance.child_plugin_instances = []
        renderer = type("Renderer", (CardRenderMixin, Terminal), {})()
        renderer.render({}, instance, None)
        rendered = render_to_string("djangocms_frontend/bootstrap5/card.html", {"instance": instance})
        self.assertIn('<div class="col mb-3">', rendered)
        self.assertIn("h-100", instance._additional_classes)
        parent.get_plugin_instance.assert_called_once()

    def test_carousel_does_not_add_empty_transition(self):
        from unittest.mock import Mock
        from djangocms_frontend.contrib.carousel.frameworks.bootstrap5 import CarouselRenderMixin

        class Terminal:
            def render(self, context, instance, placeholder):
                return context

        renderer = type("Renderer", (CarouselRenderMixin, Terminal), {})()
        for transition in ("slide", []):
            instance = FrontendUIItem(config={"carousel_transition": transition})
            instance.add_classes = Mock()
            renderer.render({}, instance, None)
            instance.add_classes.assert_called_once_with("carousel slide")


class TokenFormRegressionTests(TestCase):
    def container_data(self, **kwargs):
        return {
            "container_type": "container",
            "tag_type": "div",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **kwargs,
        }

    def test_multi_valued_fields_keep_all_values(self):
        from django import forms

        from djangocms_frontend.token_forms import EntangledModelForm

        class ChoicesForm(EntangledModelForm):
            choices = forms.MultipleChoiceField(choices=[("a", "A"), ("b", "B")])

            class Meta:
                model = FrontendUIItem
                entangled_fields = {"config": ["choices"]}
                untangled_fields = ()

        form = ChoicesForm(data=QueryDict("choices=a&choices=b"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["choices"], ["a", "b"])

    def test_projected_multi_values_are_written_back_as_lists(self):
        query = QueryDict("container_type=container&tag_type=div&padding_devices=xs", mutable=True)
        query.setlist("margin_devices", ["xs", "2xl"])
        form = GridContainerForm(data=query)
        self.assertEqual(form.data.getlist("margin_devices"), ["xs", "xxl"])
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["margin_devices"], ["xs", "2xl"])

    def test_hidden_multi_select_keeps_all_values(self):
        from django import forms

        class HiddenDevicesForm(GridContainerForm):
            class Meta(GridContainerForm.Meta):
                model = FrontendUIItem

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields["margin_devices"].widget = forms.MultipleHiddenInput()

        HiddenDevicesForm.base_fields["margin_devices"].widget = forms.MultipleHiddenInput()
        query = QueryDict("container_type=container&tag_type=div&padding_devices=xs", mutable=True)
        query.setlist("margin_devices", ["xs", "2xl"])
        form = HiddenDevicesForm(data=query)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["margin_devices"], ["xs", "2xl"])

    def test_form_shows_the_rendered_value_of_conflicting_keys(self):
        for config in ({"row_cols_2xl": 3, "row_cols_xxl": 2}, {"row_cols_xxl": 2, "row_cols_2xl": 3}):
            with self.subTest(config=config):
                form = GridRowForm(instance=FrontendUIItem(config=config))
                self.assertEqual(form.initial["row_cols_xxl"], 3)

    def test_conflict_on_disabled_or_removed_field_does_not_block_save(self):
        for change in ("disable", "remove"):
            with self.subTest(change=change):
                form = GridRowForm(
                    instance=FrontendUIItem(config={"row_cols_2xl": 3, "row_cols_xxl": 2}),
                    data={"margin_devices": ["xs"], "padding_devices": ["xs"]},
                )
                if change == "disable":
                    form.fields["row_cols_xxl"].disabled = True
                else:
                    del form.fields["row_cols_xxl"]
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], 3)

    def test_equivalent_alias_values_are_not_a_conflict(self):
        self.assertEqual(tokens.resolve_aliases({"row_cols_xxl": "6", "row_cols_2xl": 6})[1], [])
        self.assertEqual(tokens.resolve_aliases({"row_cols_xxl": "6", "row_cols_2xl": 4})[1], ["row_cols_2xl"])

    def test_spacing_projection_writes_only_widget_parts(self):
        form = GridContainerForm(data=self.container_data(margin_x="mx-3"))
        self.assertNotIn("margin_x", form.data)
        self.assertIn("margin_x_0", form.data)

    def test_parent_lookup_accepts_plugin_subclasses(self):
        from djangocms_frontend.contrib.tabs.cms_plugins import TabPlugin
        from djangocms_frontend.models import is_plugin_type

        class MyTabPlugin(TabPlugin):
            pass

        with patch("cms.plugin_pool.plugin_pool.get_plugin", return_value=MyTabPlugin):
            self.assertTrue(is_plugin_type("MyTabPlugin", "TabPlugin"))
        with patch("cms.plugin_pool.plugin_pool.get_plugin", side_effect=KeyError):
            self.assertFalse(is_plugin_type("UnknownPlugin", "TabPlugin"))
        self.assertFalse(is_plugin_type("CardPlugin", "TabPlugin"))

    def test_bad_token_on_removed_field_does_not_discard_edits(self):
        form = GridContainerForm(
            instance=FrontendUIItem(config={"container_type": "container"}),
            data=self.container_data(
                container_type="container-fluid",
                padding_x={"property": "padding", "side": "horizontal", "size": "rem-0.75"},
            ),
        )
        del form.fields["padding_x"]
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["container_type"], "fluid")

    def test_form_clean_runs_alongside_token_errors(self):
        class CheckedForm(GridContainerForm):
            class Meta(GridContainerForm.Meta):
                model = FrontendUIItem

            def clean(self):
                self.add_error(None, "form-level check")
                return super().clean()

        form = CheckedForm(
            data=self.container_data(padding_x={"property": "padding", "side": "horizontal", "size": "rem-0.75"})
        )
        self.assertFalse(form.is_valid())
        self.assertIn("padding_x", form.errors)
        self.assertIn("form-level check", form.non_field_errors())

    def test_prefixed_form_projects_canonical_input(self):
        data = {f"p-{key}": value for key, value in self.container_data(container_type="bounded").items()}
        data["p-margin_devices"] = ["xs", "2xl"]
        query = QueryDict(mutable=True)
        for key, value in data.items():
            query.setlist(key, value if isinstance(value, list) else [value])
        form = GridContainerForm(data=query, prefix="p")
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["container_type"], "bounded")
        self.assertEqual(form.cleaned_data["config"]["margin_devices"], ["xs", "2xl"])

    def test_bad_defaults_are_skipped_not_mixed_in(self):
        instance = FrontendUIItem(config={})
        with patch.dict("djangocms_frontend.models.PLUGIN_DEFAULTS", {"FrontendUIItem": {tokens.VERSION_KEY: 2}}):
            with self.assertLogs("djangocms_frontend.models", "WARNING"):
                instance.initialize_from_form(GridRowForm)
        self.assertEqual(instance.config[tokens.VERSION_KEY], 1)
        self.assertIn("gutters", instance.config)

    def test_unreadable_configuration_is_left_untouched(self):
        config = {tokens.VERSION_KEY: 2, "row_cols_xxl": 3}
        instance = FrontendUIItem(config=deepcopy(config))
        with self.assertLogs("djangocms_frontend.models", "WARNING"):
            instance.initialize_from_form(GridRowForm)
        self.assertEqual(instance.config, config)

    def test_adapter_is_read_at_call_time(self):
        instance = FrontendUIItem(config={"container_type": "bounded"})
        with patch("djangocms_frontend.settings.token_adapter", None):
            self.assertEqual(instance.get_framework_value("container_type"), "bounded")


class ReviewBoundaryFixTests(TestCase):
    def container_data(self, **extra):
        return {
            "container_type": "container",
            "tag_type": "div",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **extra,
        }

    def test_native_spacing_is_decompressed_with_or_without_prefix(self):
        for prefix in (None, "p"):
            with self.subTest(prefix=prefix):
                data = self.container_data(margin_x="mx-3", padding_y="pt-2")
                if prefix:
                    data = {f"{prefix}-{key}": value for key, value in data.items()}
                form = GridContainerForm(data=data, prefix=prefix)
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["margin_x"], tokens.normalize_value("margin_x", "mx-3"))
                self.assertEqual(form.cleaned_data["config"]["padding_y"], tokens.normalize_value("padding_y", "pt-2"))

    def test_disabled_stored_tokens_are_preserved_and_posted_values_ignored(self):
        for field, token in (
            ("background_context", "surface-3"),
            ("background_context", "inverse"),
            ("padding_x", {"property": "padding", "side": "horizontal", "size": "rem-0.75"}),
        ):
            with self.subTest(field=field, token=token):
                instance = FrontendUIItem(config=tokens.normalize_config({field: token}))
                form = GridContainerForm(
                    instance=instance, data=self.container_data(container_type="container-fluid", **{field: "accent"})
                )
                form.fields[field].disabled = True
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"][field], token)
                self.assertEqual(form.cleaned_data["config"]["container_type"], "fluid")

    def test_accent_is_unsupported_for_all_color_fields(self):
        for field in tokens.COLOR_FIELDS:
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    adapter.value(field, "accent")
                self.assertEqual(adapter.field_value(FrontendUIItem(config={field: "accent"}), field), "")
        self.assertEqual(adapter.value("alert_context", "project-brand"), "project-brand")

    def test_accent_is_a_field_error(self):
        form = GridContainerForm(data=self.container_data(background_context="accent"))
        self.assertFalse(form.is_valid())
        self.assertIn("background_context", form.errors)
        self.assertFalse(form.non_field_errors())

    def test_migration_reports_accent_and_leaves_it_untouched(self):
        item = FrontendUIItem.objects.create(plugin_type="GridRowPlugin", config={"alert_context": "accent"})
        stdout, stderr = StringIO(), StringIO()
        call_command("frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=stdout, stderr=stderr)
        self.assertIn("1 skipped", stdout.getvalue())
        self.assertIn("accent", stderr.getvalue())
        item.refresh_from_db()
        self.assertEqual(item.config, {"alert_context": "accent"})
        with self.assertRaises(CommandError):
            call_command(
                "frontend",
                "migrate",
                "--from",
                "bootstrap5",
                "--to",
                "universal",
                "--fail-on-unmapped",
                stdout=StringIO(),
                stderr=StringIO(),
            )


class SpacingValidationRegressionTests(TestCase):
    def test_rejected_spacing_fields_report_errors_without_crashing(self):
        from djangocms_frontend.contrib.utilities.forms import SpacingForm

        for field, data in (
            ("space_size", {"space_property": "padding", "space_size": "rem-0.75"}),
            ("space_property", {"space_property": "invalid", "space_size": "rem-1"}),
        ):
            with self.subTest(field=field):
                form = SpacingForm(data={"tag_type": "div", "space_sides": "all", **data})
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
                self.assertFalse(form.non_field_errors())

    def test_disabled_padding_property_still_rejects_auto_size(self):
        from djangocms_frontend.contrib.utilities.forms import SpacingForm

        config = tokens.normalize_config({"space_property": "padding", "space_sides": "all", "space_size": "rem-1"})
        instance = FrontendUIItem(config=deepcopy(config))
        form = SpacingForm(instance=instance, data={"space_size": "auto", "space_sides": "all", "tag_type": "div"})
        form.fields["space_property"].disabled = True
        self.assertFalse(form.is_valid())
        self.assertIn("space_size", form.errors)
        self.assertIn("Padding does not have an auto spacing", str(form.errors))
        self.assertEqual(instance.config, config)

    def test_disabled_property_is_native_during_clean_and_canonical_when_saved(self):
        from djangocms_frontend.contrib.utilities.forms import SpacingForm

        class CheckedSpacingForm(SpacingForm):
            class Meta(SpacingForm.Meta):
                model = FrontendUIItem

            def clean(self):
                self.property_seen_during_clean = self.cleaned_data.get("space_property")
                return super().clean()

        for prop, expected in (("padding", "p"), ("margin", "m")):
            with self.subTest(prop=prop):
                form = CheckedSpacingForm(
                    instance=FrontendUIItem(config=tokens.normalize_config({"space_property": prop})),
                    data={"space_property": "invalid", "space_size": "rem-1", "space_sides": "all", "tag_type": "div"},
                )
                form.fields["space_property"].disabled = True
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.property_seen_during_clean, expected)
                self.assertEqual(form.cleaned_data["config"]["space_property"], prop)


class TokenFullReviewTests(TestCase):
    def container_data(self, **kwargs):
        return {
            "container_type": "container",
            "tag_type": "div",
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
            **kwargs,
        }

    def test_stored_model_reference_stays_selected(self):
        from filer.models import ThumbnailOption

        from djangocms_frontend.contrib.image.forms import ImageForm

        option = ThumbnailOption.objects.create(name="square", width=100, height=100, crop=True, upscale=True)
        instance = FrontendUIItem(
            config={"thumbnail_options": {"pk": option.pk, "model": "filer.ThumbnailOption"}, "container_type": "x"}
        )
        form = ImageForm(instance=instance)
        self.assertEqual(form.initial["thumbnail_options"], option)
        self.assertIn(f'value="{option.pk}" selected', str(form["thumbnail_options"]))

    def test_viewport_height_round_trips(self):
        instance = FrontendUIItem(config=tokens.normalize_config({"size_y": "viewport"}))
        form = GridContainerForm(instance=instance)
        self.assertEqual(form.initial["size_y"], "vh-100")
        form = GridContainerForm(instance=instance, data=self.container_data(size_y="vh-100"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["size_y"], "viewport")

    def test_unlisted_stored_value_survives_an_unchanged_save(self):
        instance = FrontendUIItem(config={"container_type": "project-container"})
        form = GridContainerForm(instance=instance)
        self.assertEqual(form.initial["container_type"], "project-container")
        form = GridContainerForm(instance=instance, data=self.container_data(container_type="project-container"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["container_type"], "project-container")

    def test_project_declared_fields_are_not_tokens(self):
        from django import forms

        from djangocms_frontend.token_forms import EntangledModelForm, project_fields

        class ComponentForm(EntangledModelForm):
            size_x = forms.ChoiceField(choices=[("50", "Half"), ("100", "Full")])
            link_type = forms.ChoiceField(choices=[("primary", "Primary"), ("ghost", "Ghost")])

            class Meta:
                model = FrontendUIItem
                entangled_fields = {"config": ["size_x", "link_type"]}
                untangled_fields = ()

        self.assertEqual(project_fields(ComponentForm), {"size_x", "link_type"})
        self.assertNotIn("size_x", project_fields(GridContainerForm))
        form = ComponentForm(data={"size_x": "50", "link_type": "ghost"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["size_x"], "50")
        self.assertEqual(form.cleaned_data["config"]["link_type"], "ghost")
        instance = FrontendUIItem(config={})
        instance.initialize_from_form(ComponentForm)
        self.assertNotIn("percent-50", instance.config.values())

    def test_equal_alias_values_of_different_types_do_not_conflict(self):
        self.assertEqual(tokens.normalize_config({"xxl_col": "6", "2xl_col": 6})["2xl_col"], 6)
        with self.assertRaises(ValueError):
            tokens.normalize_config({"xxl_col": "6", "2xl_col": 4})

    def test_explicit_none_prefix_keeps_the_class_prefix(self):
        class PrefixedForm(GridContainerForm):
            prefix = "p"

            class Meta(GridContainerForm.Meta):
                model = FrontendUIItem

        data = {f"p-{key}": value for key, value in self.container_data(container_type="bounded").items()}
        form = PrefixedForm(data=data, prefix=None)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["container_type"], "bounded")


class ProjectBoundaryRegressionTests(TestCase):
    def project_form(self):
        from django import forms
        from djangocms_frontend.token_forms import EntangledModelForm

        class ProjectForm(EntangledModelForm):
            size_x = forms.CharField(initial="50")
            row_cols_xxl = forms.CharField(required=False)
            row_cols_2xl = forms.CharField(required=False)

            class Meta:
                model = FrontendUIItem
                entangled_fields = {"config": ["size_x", "row_cols_xxl", "row_cols_2xl"]}
                untangled_fields = ()

        return ProjectForm

    def test_plugin_tag_preserves_project_field_values_and_names(self):
        from django.template import engines

        project_form = self.project_form()

        class ProjectPlugin:
            form = project_form
            model = FrontendUIItem

            def render(self, context, instance, placeholder):
                context["instance"] = instance
                return context

            def _get_render_template(self, *args):
                return "project-probe"

        entry = {
            "class": ProjectPlugin,
            "defaults": {"config": {}},
            "templates": {
                "project-probe": engines["django"].from_string(
                    "{{ instance.size_x }}|{{ instance.row_cols_xxl }}|{{ instance.row_cols_2xl }}"
                )
            },
        }
        with patch.dict("djangocms_frontend.plugin_tag.plugin_tag_pool", {"project-probe": entry}):
            rendered = Template(
                '{% load frontend %}{% plugin "project-probe" size_x="50" '
                'row_cols_xxl="first" row_cols_2xl="second" %}{% endplugin %}'
            ).render(Context())
        self.assertEqual(rendered, "50|first|second")

    def test_initialization_preserves_project_alias_names_in_every_source(self):
        project_form = self.project_form()
        values = {"row_cols_xxl": "first", "row_cols_2xl": "second"}
        for source in ("stored", "model", "settings"):
            with self.subTest(source=source):
                instance = FrontendUIItem(config=deepcopy(values) if source == "stored" else {})
                with patch.object(FrontendUIItem, "default_config", values if source == "model" else {}, create=True):
                    with patch(
                        "djangocms_frontend.models.PLUGIN_DEFAULTS",
                        {
                            "FrontendUIItem": values if source == "settings" else {},
                        },
                    ):
                        instance.initialize_from_form(project_form)
                self.assertEqual(instance.config["row_cols_xxl"], "first")
                self.assertEqual(instance.config["row_cols_2xl"], "second")

    def test_form_preserves_disabled_project_alias_fields(self):
        project_form = self.project_form()
        instance = FrontendUIItem(config={"row_cols_xxl": "first", "row_cols_2xl": "second"})
        form = project_form(instance=instance, data={"size_x": "100"})
        form.fields["row_cols_xxl"].disabled = True
        form.fields["row_cols_2xl"].disabled = True
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["row_cols_xxl"], "first")
        self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], "second")

    def test_explicit_initial_wins_in_native_and_canonical_spelling(self):
        for initial in ("container-fluid", "fluid"):
            with self.subTest(initial=initial):
                form = GridContainerForm(
                    instance=FrontendUIItem(config={"container_type": "bounded"}),
                    initial={"container_type": initial},
                )
                self.assertEqual(form.initial["container_type"], "container-fluid")

    def test_explicit_grid_initial_wins_across_key_aliases(self):
        for field in ("row_cols_xxl", "row_cols_2xl"):
            with self.subTest(field=field):
                form = GridRowForm(
                    instance=FrontendUIItem(config={"row_cols_2xl": 3}),
                    initial={field: 5},
                )
                self.assertEqual(form.initial["row_cols_xxl"], 5)


class TokenAdapterReviewTests(TestCase):
    def test_project_native_value_sharing_a_token_name_is_passed_through(self):
        from djangocms_frontend.frameworks import bootstrap5 as framework

        instance = FrontendUIItem(config={"alert_context": "accent", "alert_shadow": "xl"})
        with self.assertRaises(ValueError):
            adapter.value("alert_context", "accent")
        self.assertEqual(adapter.field_value(instance, "alert_context"), "")
        colors = (*framework.COLOR_STYLE_CHOICES, ("accent", "Accent"))
        shadows = (*framework.SHADOW_CHOICES, ("xl", "XL"))
        with (
            patch.object(framework, "COLOR_STYLE_CHOICES", colors),
            patch.object(framework, "SHADOW_CHOICES", shadows),
        ):
            self.assertEqual(adapter.value("alert_context", "accent"), "accent")
            self.assertEqual(adapter.field_value(instance, "alert_context"), "accent")
            self.assertEqual(adapter.field_value(instance, "alert_shadow"), "xl")

    def test_unexpressible_stored_token_is_kept_unless_replaced_or_cleared(self):
        instance = FrontendUIItem(config=tokens.normalize_config({"background_context": "surface-3"}))
        form = GridContainerForm(instance=instance)
        self.assertIn("surface-3", [value for value, _ in form.fields["background_context"].choices])
        container = TokenFullReviewTests.container_data
        for posted, expected in (("surface-3", "surface-3"), ("primary", "primary"), ("", "")):
            with self.subTest(posted=posted):
                form = GridContainerForm(instance=instance, data=container(self, background_context=posted))
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["background_context"], expected)

    def test_stale_value_of_a_non_token_field_is_not_offered(self):
        from djangocms_frontend.contrib.link.forms import LinkForm

        form = LinkForm(instance=FrontendUIItem(config={"template": "removed"}))
        self.assertNotIn("removed", [value for value, _ in form.fields["template"].choices])

    def test_project_field_cache_does_not_keep_form_classes_alive(self):
        import gc
        import weakref

        from djangocms_frontend.token_forms import _project_fields, project_fields

        form_class = type("RequestForm", (GridContainerForm,), {})
        project_fields(form_class)
        self.assertIn(form_class, _project_fields)
        ref = weakref.ref(form_class)
        del form_class
        gc.collect()
        self.assertIsNone(ref())

    def test_tab_item_under_a_project_tab_container(self):
        from djangocms_frontend.contrib.tabs.frameworks.bootstrap5 import TabItemRenderMixin

        class Base:
            def render(self, context, instance, placeholder):
                return context

        class Renderer(TabItemRenderMixin, Base):
            pass

        container = SimpleNamespace(config={"tab_type": "nav-tabs"}, tab_effect="fade", tab_index=1)
        parent = SimpleNamespace(plugin_type="ProjectTabsPlugin", get_plugin_instance=lambda: (container, None))
        instance = FrontendUIItem(config={})
        with patch.object(FrontendUIItem, "parent", parent):
            Renderer().render({"parentloop": {"counter": 1}}, instance, None)
        self.assertTrue({"tab-pane", "fade", "bg-body", "show", "active"} <= set(instance._additional_classes))

    def test_spacing_render_uses_the_instance_override(self):
        from djangocms_frontend.contrib.utilities.frameworks.bootstrap5 import SpacingRenderMixin

        class Base:
            def render(self, context, instance, placeholder):
                return context

        class Renderer(SpacingRenderMixin, Base):
            pass

        instance = FrontendUIItem(config={})
        instance.get_base_css_class = lambda: "custom-space"
        Renderer().render({}, instance, None)
        self.assertIn("custom-space", instance._additional_classes)


class DisabledInitialRegressionTests(TestCase):
    def test_disabled_explicit_container_initial_matches_saved_value(self):
        for initial in ("fluid", "container-fluid"):
            with self.subTest(initial=initial):
                form = GridContainerForm(
                    instance=FrontendUIItem(config={"container_type": "bounded"}),
                    initial={"container_type": initial},
                    data={
                        "container_type": "container-full",
                        "tag_type": "div",
                        "margin_devices": ["xs"],
                        "padding_devices": ["xs"],
                    },
                )
                form.fields["container_type"].disabled = True
                self.assertEqual(form.initial["container_type"], "container-fluid")
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["container_type"], "fluid")

    def test_disabled_explicit_initial_preserves_requested_semantic_role(self):
        for stored, initial in (("inverse", "neutral-dark"), ("neutral-dark", "inverse")):
            with self.subTest(stored=stored, initial=initial):
                form = GridContainerForm(
                    instance=FrontendUIItem(config={"background_context": stored}),
                    initial={"background_context": initial},
                    data={
                        "container_type": "container",
                        "background_context": "primary",
                        "tag_type": "div",
                        "margin_devices": ["xs"],
                        "padding_devices": ["xs"],
                    },
                )
                form.fields["background_context"].disabled = True
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["background_context"], initial)

    def test_disabled_explicit_grid_initial_accepts_either_key_spelling(self):
        for name in ("row_cols_xxl", "row_cols_2xl"):
            with self.subTest(name=name):
                form = GridRowForm(
                    instance=FrontendUIItem(config={"row_cols_2xl": 3}),
                    initial={name: 5},
                    data={"row_cols_xxl": 7, "margin_devices": ["xs"], "padding_devices": ["xs"]},
                )
                form.fields["row_cols_xxl"].disabled = True
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["row_cols_2xl"], 5)


class TokenOwnershipReviewTests(TestCase):
    def test_project_native_value_wins_over_a_supported_token_mapping(self):
        from djangocms_frontend.frameworks import bootstrap5 as framework

        self.assertEqual(adapter.value("background_shadow", "md"), "reg")
        shadows = (*framework.SHADOW_CHOICES, ("md", "M (theme)"))
        colors = (*framework.COLOR_STYLE_CHOICES, ("inverse", "Inverse"))
        with (
            patch.object(framework, "SHADOW_CHOICES", shadows),
            patch.object(framework, "COLOR_STYLE_CHOICES", colors),
        ):
            self.assertEqual(adapter.value("background_shadow", "md"), "md")
            self.assertEqual(adapter.value("alert_context", "inverse"), "inverse")

    def test_migration_reads_all_rows_in_batches(self):
        from djangocms_frontend.management import universal_migration

        items = [
            FrontendUIItem.objects.create(config={"xxl_col": n}, plugin_type="GridColumnPlugin", language="en")
            for n in range(1, 6)
        ]
        with patch.object(universal_migration, "BATCH_SIZE", 2):
            stdout = StringIO()
            call_command(
                "frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=stdout, stderr=StringIO()
            )
        self.assertIn("Migrated 5 configurations", stdout.getvalue())
        for n, item in enumerate(items, 1):
            item.refresh_from_db()
            self.assertEqual(item.config["2xl_col"], n)

    def test_type_built_project_form_keeps_its_fields(self):
        from django import forms

        from djangocms_frontend.contrib.grid.forms import GridColumnForm, GridRowForm
        from djangocms_frontend.token_forms import EntangledModelForm, project_fields

        meta = type(
            "Meta",
            (),
            {"model": FrontendUIItem, "entangled_fields": {"config": ["size_x"]}, "untangled_fields": ()},
        )
        form_class = type(
            "ProjectForm",
            (EntangledModelForm,),
            {"size_x": forms.ChoiceField(choices=[("25", "Quarter")]), "Meta": meta},
        )
        self.assertEqual(project_fields(form_class), {"size_x"})
        self.assertEqual(project_fields(GridRowForm), frozenset())
        self.assertEqual(project_fields(GridColumnForm), frozenset())
        form = form_class(data={"size_x": "25"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["config"]["size_x"], "25")

    def test_plugin_type_match_requires_the_registered_plugin_class(self):
        from cms.plugin_base import CMSPluginBase

        from djangocms_frontend.models import is_plugin_type

        class CardPlugin(CMSPluginBase):  # an unrelated class sharing the name
            pass

        class ThirdPartyPlugin(CardPlugin):
            pass

        from cms.plugin_pool import plugin_pool

        real_get_plugin = plugin_pool.get_plugin

        def get_plugin(name):
            return ThirdPartyPlugin if name == "ThirdPartyPlugin" else real_get_plugin(name)

        with patch.object(plugin_pool, "get_plugin", side_effect=get_plugin):
            self.assertFalse(is_plugin_type("ThirdPartyPlugin", "CardPlugin"))
            self.assertTrue(is_plugin_type("CardPlugin", "CardPlugin"))


class StoredSpacingWidgetRegressionTests(TestCase):
    def spacing(self):
        return {"property": "padding", "side": "horizontal", "size": "rem-0.75"}

    def container_data(self, side="px", size="rem-0.75", prefix=None):
        data = {
            "container_type": "container",
            "tag_type": "div",
            "plugin_title_0": "on",
            "plugin_title_1": "Edited",
            "padding_x_0": side,
            "padding_x_1": size,
            "margin_devices": ["xs"],
            "padding_devices": ["xs"],
        }
        return {f"{prefix}-{key}": value for key, value in data.items()} if prefix else data

    def test_stored_non_native_spacing_is_visible_and_survives_a_title_edit(self):
        for prefix in (None, "p"):
            with self.subTest(prefix=prefix):
                instance = FrontendUIItem(config={"padding_x": self.spacing()})
                initial = GridContainerForm(instance=instance, prefix=prefix)
                self.assertEqual(
                    initial.fields["padding_x"].widget.decompress(initial.initial["padding_x"]), ["px", "rem-0.75"]
                )
                self.assertIn('value="rem-0.75" selected', str(initial["padding_x"]))
                form = GridContainerForm(instance=instance, data=self.container_data(prefix=prefix), prefix=prefix)
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["padding_x"], self.spacing())
                self.assertEqual(form.cleaned_data["config"]["plugin_title"], {"show": True, "title": "Edited"})

    def test_editor_can_replace_or_clear_stored_non_native_spacing(self):
        for side, size, expected in (("px", "3", tokens.normalize_value("padding_x", "px-3")), ("", "", "")):
            with self.subTest(side=side, size=size):
                instance = FrontendUIItem(config={"padding_x": self.spacing()})
                form = GridContainerForm(instance=instance, data=self.container_data(side, size))
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["config"]["padding_x"], expected)

    def test_new_non_native_spacing_still_fails_validation(self):
        form = GridContainerForm(data=self.container_data())
        self.assertFalse(form.is_valid())
        self.assertIn("padding_x", form.errors)
        with self.assertRaises(ValueError):
            adapter.value("padding_x", self.spacing())


class TokenRenderReviewTests(TestCase):
    def test_migration_skips_plugins_whose_form_cannot_read_tokens(self):
        from django import forms as django_forms
        from entangled.forms import EntangledModelForm as PlainEntangledModelForm

        from djangocms_frontend.common import MarginFormMixin
        from djangocms_frontend.management import universal_migration

        class PlainForm(MarginFormMixin, PlainEntangledModelForm):
            title = django_forms.CharField(required=False)

            class Meta:
                model = FrontendUIItem
                entangled_fields = {"config": ["title"]}
                untangled_fields = ()

        item = FrontendUIItem.objects.create(plugin_type="ThirdPartyPlugin", config={"margin_x": "mx-3"})
        stdout, stderr = StringIO(), StringIO()
        with patch.object(universal_migration, "plugin_form", return_value=PlainForm):
            call_command(
                "frontend", "migrate", "--from", "bootstrap5", "--to", "universal", stdout=stdout, stderr=stderr
            )
        self.assertIn("1 skipped", stdout.getvalue())
        self.assertIn("ThirdPartyPlugin has no form reading universal tokens", stderr.getvalue())
        item.refresh_from_db()
        self.assertEqual(item.config, {"margin_x": "mx-3"})

    def test_legacy_value_is_kept_when_its_target_is_another_project_choice(self):
        from djangocms_frontend.frameworks import bootstrap5 as framework

        self.assertEqual(tokens.normalize_value("background_shadow", "reg"), "md")
        shadows = (*framework.SHADOW_CHOICES, ("md", "M (theme)"))
        with patch.object(framework, "SHADOW_CHOICES", shadows):
            self.assertEqual(tokens.normalize_value("background_shadow", "reg"), "reg")
            self.assertEqual(adapter.value("background_shadow", "reg"), "reg")
            self.assertEqual(adapter.value("background_shadow", "md"), "md")
        # Targets that are not project choices are still converted.
        self.assertEqual(tokens.normalize_value("alert_context", "light"), "neutral-light")

    def test_rendering_passes_project_fields_through(self):
        instance = FrontendUIItem(plugin_type="ProjectPlugin", config={"container_type": "fluid"})
        self.assertEqual(adapter.field_value(instance, "container_type"), "container-fluid")
        with patch.object(adapter, "_project_fields", return_value=frozenset({"container_type"})):
            self.assertEqual(adapter.field_value(instance, "container_type"), "fluid")

    def test_template_plugin_type_filter_and_parent_tag_guard(self):
        from cms.plugin_pool import plugin_pool

        from djangocms_frontend.contrib.card.cms_plugins import CardPlugin

        class ProjectCardPlugin(CardPlugin):
            pass

        real_get_plugin = plugin_pool.get_plugin

        def get_plugin(name):
            return ProjectCardPlugin if name == "ProjectCardPlugin" else real_get_plugin(name)

        template = Template(
            '{% load frontend_tokens %}{% if plugin_type|is_plugin_type:"CardPlugin" %}card{% endif %}'
            '|{% parent_framework_value instance "CardLayoutPlugin" "card_type" %}'
        )
        with patch.object(plugin_pool, "get_plugin", side_effect=get_plugin):
            for plugin_type, expected in (("ProjectCardPlugin", "card|"), ("GridRowPlugin", "|"), ("", "|")):
                with self.subTest(plugin_type=plugin_type):
                    rendered = template.render(Context({"plugin_type": plugin_type, "instance": object()}))
                    self.assertEqual(rendered, expected)


class StrictAndStandaloneRegressionTests(TestCase):
    def test_strict_migration_rolls_back_before_unreadable_plugin(self):
        from entangled.forms import EntangledModelForm as PlainEntangledModelForm
        from djangocms_frontend.management import universal_migration

        for unreadable_form in (None, PlainEntangledModelForm):
            with self.subTest(form=unreadable_form):
                valid = FrontendUIItem.objects.create(
                    plugin_type="GridContainerPlugin", config={"container_type": "container"}
                )
                unreadable = FrontendUIItem.objects.create(
                    plugin_type="UnavailablePlugin", config={"container_type": "container"}
                )
                resolve = universal_migration.plugin_form

                def form_for(plugin_type):
                    return unreadable_form if plugin_type == "UnavailablePlugin" else resolve(plugin_type)

                with patch.object(universal_migration, "plugin_form", side_effect=form_for):
                    with patch.object(universal_migration, "BATCH_SIZE", 1):
                        with self.assertRaisesMessage(
                            CommandError, "UnavailablePlugin has no form reading universal tokens"
                        ):
                            call_command(
                                "frontend",
                                "migrate",
                                "--from",
                                "bootstrap5",
                                "--to",
                                "universal",
                                "--fail-on-unmapped",
                                stdout=StringIO(),
                                stderr=StringIO(),
                            )
                valid.refresh_from_db()
                unreadable.refresh_from_db()
                self.assertEqual(valid.config, {"container_type": "container"})
                self.assertEqual(unreadable.config, {"container_type": "container"})
                unreadable.delete()
                valid.delete()

    def test_tokens_normalize_without_django_or_project_settings(self):
        import os
        import subprocess
        import sys
        from pathlib import Path

        env = {key: value for key, value in os.environ.items() if key != "DJANGO_SETTINGS_MODULE"}
        result = subprocess.run(
            [
                sys.executable,
                "-S",
                "-c",
                """
import sys
from djangocms_frontend import tokens
assert tokens.normalize_config({"container_type": "container", "background_shadow": "reg"}) == {
    "container_type": "bounded", "background_shadow": "md", "_frontend_tokens": 1,
}
assert "django" not in sys.modules
assert "djangocms_frontend.settings" not in sys.modules
""",
            ],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class TokenOwnershipGuardTests(TestCase):
    def test_built_in_plugin_forms_declare_no_project_fields(self):
        # Guards ownership detection, e.g. for forms built with type().
        from cms.plugin_pool import plugin_pool

        from djangocms_frontend.token_forms import EntangledModelForm, project_fields

        checked = 0
        for name, plugin in plugin_pool.plugins.items():
            form = getattr(plugin, "form", None)
            # Component forms report the component's module (they hold its own fields).
            if isinstance(form, type) and form.__module__.startswith("djangocms_frontend."):
                if issubclass(form, EntangledModelForm):
                    with self.subTest(plugin=name):
                        self.assertEqual(project_fields(form), frozenset())
                    checked += 1
        self.assertGreater(checked, 20)

    def test_type_built_forms_report_their_callers_module(self):
        from djangocms_frontend.contrib.grid.forms import GridColumnForm, GridRowForm

        self.assertEqual(GridRowForm.__module__, "djangocms_frontend.contrib.grid.forms")
        self.assertEqual(GridColumnForm.__module__, "djangocms_frontend.contrib.grid.forms")
        project_form = type("ProjectRowForm", (GridRowForm,), {})
        self.assertEqual(project_form.__module__, __name__)

    def test_non_object_config_opens_and_is_reported_on_save(self):
        from djangocms_frontend.contrib.alert.forms import AlertForm

        for config in (["x"], "abc"):
            with self.subTest(config=config):
                instance = FrontendUIItem(config=config)
                AlertForm(instance=instance)
                form = AlertForm(instance=instance, data={"alert_context": "primary", "tag_type": "div"})
                self.assertFalse(form.is_valid())
                self.assertIn("must be an object", str(form.non_field_errors()))

    def test_empty_link_type_migrates(self):
        item = FrontendUIItem.objects.create(plugin_type="TextLinkPlugin", config={"link_type": "", "name": "x"})
        stdout = StringIO()
        call_command(
            "frontend", "migrate", "--from", "bootstrap5", "--to", "universal", "--fail-on-unmapped", stdout=stdout
        )
        self.assertIn("Migrated 1", stdout.getvalue())
        item.refresh_from_db()
        self.assertEqual(item.config["link_type"], "")
