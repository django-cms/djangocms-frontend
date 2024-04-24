from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .base import SubcommandsCommand

User = get_user_model()


class SyncPermissions(SubcommandsCommand):
    help = "Sets the permissions for all plugins to those of djangocms_frontend.models.FrontendUIItem"
    command_name = "sync_permissions"

    def add_arguments(self, parser):
        parser.add_argument("scope", choices=["users", "groups"])

    def handle(self, *args, **options):
        if options["interactive"]:
            self.stdout.write(
                """This command changes permissions for djangocms-frontend plugins.
Changes cannot be undone. Are you sure you want to proceed?
"""
            )
            ok_to_delete = input("Type 'yes' to continue, or 'no' to cancel: ")
        else:
            ok_to_delete = "yes"

        if ok_to_delete != "yes":
            self.stdout.write(self.style.ERROR("Aborted."))
            return

        dcf_models = [m for m in apps.get_models() if m.__module__.startswith("djangocms_frontend.")]
        reference_model = [m for m in dcf_models if m.__name__ == "FrontendUIItem"][0]
        dcf_models.remove(reference_model)
        ctype = ContentType.objects.get(
            app_label=reference_model._meta.app_label,
            model=reference_model._meta.object_name.lower(),
        )
        permission_set = Permission.objects.filter(content_type=ctype)
        if "users" in options["scope"]:
            for user in User.objects.all():
                self.stdout.write(self.style.SUCCESS(f"Snycing {user}"))
                reduced = permission_set.filter(user=user)
                reduced = [perm.codename.split("_")[0] for perm in reduced]
                if reduced:
                    self.stdout.write(self.style.NOTICE(f"... has {', '.join(reduced)}"))
                for model in dcf_models:
                    perms = _get_all_permissions(model._meta)
                    for perm, name in perms:
                        ok = perm.split("_")[0] in reduced
                        ctype = ContentType.objects.get(
                            app_label=model._meta.app_label,
                            model=model._meta.object_name.lower(),
                        )
                        new_perm, created = Permission.objects.get_or_create(
                            codename=perm,
                            content_type=ctype,
                            defaults=dict(name=name),
                        )
                        if created:
                            self.stdout.write(self.style.WARNING(f"Created permission {new_perm}"))
                        if ok:
                            if not user.user_permissions.filter(codename=new_perm.codename, content_type=ctype):
                                self.stdout.write(self.style.NOTICE(f"Added {new_perm} for {user}"))
                                user.user_permissions.add(new_perm)
                        else:
                            if user.user_permissions.filter(codename=new_perm.codename, content_type=ctype):
                                self.stdout.write(self.style.WARNING(f"Removed {new_perm} for {user}"))
                                user.user_permissions.remove(new_perm)
                user.save()
        if "groups" in options["scope"]:
            for group in Group.objects.all():
                self.stdout.write(self.style.SUCCESS(f"Snycing {group}"))
                reduced = permission_set.filter(group=group)
                reduced = [perm.codename.split("_")[0] for perm in reduced]
                if reduced:
                    self.stdout.write(self.style.NOTICE(f"... has {', '.join(reduced)}"))
                for model in dcf_models:
                    perms = _get_all_permissions(model._meta)
                    for perm, name in perms:
                        ok = perm.split("_")[0] in reduced
                        ctype = ContentType.objects.get(
                            app_label=model._meta.app_label,
                            model=model._meta.object_name.lower(),
                        )
                        new_perm, created = Permission.objects.get_or_create(
                            codename=perm,
                            content_type=ctype,
                            defaults=dict(name=name),
                        )
                        if ok:
                            if not group.permissions.filter(codename=new_perm.codename, content_type=ctype):
                                self.stdout.write(self.style.NOTICE(f"Added {new_perm} for {group}"))
                                group.permissions.add(new_perm)
                        else:
                            if group.permissions.filter(codename=new_perm.codename, content_type=ctype):
                                self.stdout.write(self.style.WARNING(f"Removed {new_perm} for {group}"))
                                group.permissions.remove(new_perm)
                group.save()

        self.stdout.write(self.style.SUCCESS("Finished syncing permissions"))
