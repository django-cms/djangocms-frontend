from django.test import TestCase

from djangocms_frontend.contrib.grid.forms import GridColumnForm, GridContainerForm, GridRowForm


class GridFormTestCase(TestCase):
    def test_grid_container_form(self):
        form = GridContainerForm(
            data={
                "container_type": "container",
                "tag_type": "div",
                "margin_devices": ["xl"],
                "padding_devices": ["xs"],
            }
        )
        self.assertTrue(form.is_valid())
        self.assertIn("container_type", form.instance.config)
        self.assertEqual(form.instance.container_type, "container")

    def test_grid_row_form(self):
        form = GridRowForm(
            data={
                "margin_devices": ["xl"],
                "padding_devices": ["xs"],
                "row_cols_xs": 5,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertIn("row_cols_xs", form.instance.config)
        self.assertIn("row_cols_xxl", form.instance.config)
        self.assertEqual(form.instance.row_cols_xs, 5)

    def test_grid_column_form(self):
        form = GridColumnForm(
            data={
                "margin_devices": ["xl"],
                "padding_devices": ["xs"],
                "text_alignment": "",
                "xs_col": "6",
                "xl_offset": "",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertIn("md_me", form.instance.config)
        self.assertEqual(form.instance.xs_col, 6)
