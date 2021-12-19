from django.db import migrations, models

import djangocms_frontend.fields


class Migration(migrations.Migration):

    dependencies = [
        ("grid", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bootstrap5gridcolumn",
            name="lg_offset",
            field=djangocms_frontend.fields.IntegerRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bootstrap5gridcolumn",
            name="md_offset",
            field=djangocms_frontend.fields.IntegerRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bootstrap5gridcolumn",
            name="sm_offset",
            field=djangocms_frontend.fields.IntegerRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bootstrap5gridcolumn",
            name="xl_offset",
            field=djangocms_frontend.fields.IntegerRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bootstrap5gridcolumn",
            name="xs_offset",
            field=djangocms_frontend.fields.IntegerRangeField(blank=True, null=True),
        ),
    ]
