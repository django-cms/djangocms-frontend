"""Instances built outside the editing form (e.g. imports) must still expose their
declared config fields and reach a complete config via clean()."""

from django.test import TestCase

from djangocms_frontend.contrib.alert.forms import AlertForm
from djangocms_frontend.contrib.alert.models import Alert
from djangocms_frontend.contrib.card.forms import CardForm
from djangocms_frontend.contrib.card.models import Card


class SparseConfigAttributeAccessTestCase(TestCase):
    """__getattr__ returns the declared default for a field missing from config."""

    def test_declared_field_returns_default_when_absent(self):
        sparse = Alert(plugin_type="AlertPlugin", config={})
        # Would raise AttributeError before the fix:
        self.assertEqual(sparse.alert_context, AlertForm()["alert_context"].initial)

    def test_all_render_read_fields_resolve(self):
        """Every attribute the Alert bootstrap5 render reads unguarded must resolve."""
        sparse = Alert(plugin_type="AlertPlugin", config={})
        for field in ("alert_context", "alert_shadow", "alert_dismissible"):
            # Must not raise.
            getattr(sparse, field)

    def test_card_fields_resolve(self):
        sparse = Card(plugin_type="CardPlugin", config={})
        for field in ("card_alignment", "card_outline", "card_text_color", "card_full_height"):
            getattr(sparse, field)

    def test_present_value_wins_over_default(self):
        instance = Alert(plugin_type="AlertPlugin", config={"alert_context": "danger"})
        self.assertEqual(instance.alert_context, "danger")

    def test_undeclared_attribute_still_raises(self):
        sparse = Alert(plugin_type="AlertPlugin", config={})
        with self.assertRaises(AttributeError):
            sparse.definitely_not_a_field

    def test_default_is_copied_not_shared(self):
        """A mutable default handed out must not alias the cached template."""
        a = Alert(plugin_type="AlertPlugin", config={})
        b = Alert(plugin_type="AlertPlugin", config={})
        a.attributes["class"] = "mutated"
        self.assertEqual(b.attributes, {})


class CleanPopulatesConfigTestCase(TestCase):
    """clean() fills every declared field with its default, idempotently."""

    def test_clean_fills_missing_fields(self):
        sparse = Alert(plugin_type="AlertPlugin", config={})
        sparse.clean()
        self.assertIn("alert_context", sparse.config)
        self.assertIn("alert_dismissible", sparse.config)
        self.assertEqual(sparse.config["alert_context"], AlertForm()["alert_context"].initial)

    def test_clean_does_not_clobber_user_values(self):
        instance = Alert(plugin_type="AlertPlugin", config={"alert_context": "danger"})
        instance.clean()
        self.assertEqual(instance.config["alert_context"], "danger")
        # ...but still fills the rest.
        self.assertIn("alert_dismissible", instance.config)

    def test_clean_is_idempotent(self):
        sparse = Alert(plugin_type="AlertPlugin", config={})
        sparse.clean()
        first = dict(sparse.config)
        sparse.clean()
        self.assertEqual(sparse.config, first)

    def test_clean_matches_initialize_from_form_for_entangled_fields(self):
        """clean()-seeded instance has (at least) the keys initialize_from_form seeds."""
        via_form = Alert(plugin_type="AlertPlugin", config={})
        via_form.initialize_from_form(AlertForm)

        via_clean = Alert(plugin_type="AlertPlugin", config={})
        via_clean.clean()

        for key in via_form.config:
            self.assertIn(key, via_clean.config, f"{key} missing after clean()")

    def test_card_clean_fills_fields(self):
        sparse = Card(plugin_type="CardPlugin", config={})
        sparse.clean()
        self.assertIn("card_alignment", sparse.config)
        self.assertIn("card_outline", sparse.config)
