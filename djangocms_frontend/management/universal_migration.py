"""Explicit, repeatable Bootstrap 5 to universal-token data conversion."""

from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.db import connections, transaction
from django.db.models import TextField
from django.db.models.functions import Cast

from djangocms_frontend.frameworks.bootstrap5_tokens import value as bootstrap5_value
from djangocms_frontend.models import AbstractFrontendUIItem
from djangocms_frontend.token_forms import EntangledModelForm, plugin_form, project_fields
from djangocms_frontend.tokens import config_issues, normalize_config


def configuration_models():
    """Visit each concrete config table once, including abstract-base custom plugins."""
    for model in apps.get_models():
        if issubclass(model, AbstractFrontendUIItem) and not model._meta.proxy:
            if model._meta.get_field("config").model is model:
                yield model


BATCH_SIZE = 500


def plugin_token_fields(plugin_type):
    """Return the config fields a project declares itself (they are not tokens), or
    None if the plugin's form cannot read tokens: converting it would lose values.

    Only forms based on ``djangocms_frontend.token_forms.EntangledModelForm`` read
    tokens; one based on ``entangled.forms`` would show and save converted values empty.
    """
    form = plugin_form(plugin_type)
    if form is None or not issubclass(form, EntangledModelForm):
        return None
    return project_fields(form)


def migrate_to_universal(*, database, dry_run, stdout, stderr, fail_on_unmapped=False):
    if getattr(settings, "DJANGOCMS_FRONTEND_FRAMEWORK", "bootstrap5") != "bootstrap5":
        raise CommandError("Bootstrap 5 to universal conversion requires DJANGOCMS_FRONTEND_FRAMEWORK='bootstrap5'")
    changed = unchanged = skipped = 0
    skip_fields = {}  # per plugin type
    # A failure, including optimistic concurrency failure, rolls back the whole invocation.
    with transaction.atomic(using=database):
        for model in configuration_models():
            # Compare the exact stored representation, not a JSON value serialized
            # again by the ORM. SQLite JSON equality is otherwise text-sensitive.
            queryset = model._base_manager.using(database)
            oracle = connections[database].vendor == "oracle"
            if oracle:
                # Oracle JSON is a LOB: lock the source row while reading and
                # updating instead of comparing LOB values in a WHERE clause.
                queryset = queryset.select_for_update()
            else:
                queryset = queryset.annotate(_token_source=Cast("config", output_field=TextField()))
            # Read the keys first: SQLite gives no isolation between an open batched
            # cursor and updates to the same table on the same connection.
            pks = list(queryset.order_by("pk").values_list("pk", flat=True))
            items = (
                item
                for start in range(0, len(pks), BATCH_SIZE)
                for item in queryset.filter(pk__in=pks[start : start + BATCH_SIZE]).only("pk", "plugin_type", "config")
            )
            for item in items:
                if item.plugin_type not in skip_fields:
                    skip_fields[item.plugin_type] = plugin_token_fields(item.plugin_type)
                skip = skip_fields[item.plugin_type]
                if skip is None:
                    skipped += 1
                    message = (
                        f"{model._meta.label} pk={item.pk}: {item.plugin_type} has no form reading universal tokens"
                    )
                    if fail_on_unmapped:
                        raise CommandError(message)
                    stderr.write(message)
                    continue
                try:
                    canonical = normalize_config(item.config, skip=skip)
                    tokens = {field: token for field, token in canonical.items() if field not in skip}
                    issues = config_issues(tokens)
                    if not issues:
                        # A canonical token also needs a working source adapter recipe.
                        for field, token in tokens.items():
                            bootstrap5_value(field, token)
                except ValueError as exc:
                    issues = [str(exc)]
                if issues:
                    skipped += 1
                    message = f"{model._meta.label} pk={item.pk}: {'; '.join(issues)}"
                    if fail_on_unmapped:
                        raise CommandError(message)
                    stderr.write(message)
                    continue
                if canonical == item.config:
                    unchanged += 1
                    continue
                changed += 1
                if not dry_run:
                    guard = {} if oracle else {"_token_source": item._token_source}
                    updated = queryset.filter(pk=item.pk, **guard).update(config=canonical)
                    if updated != 1:
                        raise CommandError(
                            f"{model._meta.label} pk={item.pk} changed concurrently; migration rolled back"
                        )
    action = "Would migrate" if dry_run else "Migrated"
    stdout.write(f"{action} {changed} configurations; {unchanged} unchanged; {skipped} skipped.")
