from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from news.models import News


class Command(BaseCommand):
    help = "Seed user groups and permissions"

    def handle(self, *args, **kwargs):
        # Admin group
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        admin_perms = Permission.objects.all()
        admin_group.permissions.set(admin_perms)

        # Editor group
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        news_ct = ContentType.objects.get_for_model(News)
        editor_perms = Permission.objects.filter(
            content_type=news_ct,
            codename__in=["add_news", "change_news", "delete_news", "view_news"],
        )
        editor_group.permissions.set(editor_perms)

        # Reader group
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        view_perm = Permission.objects.get(content_type=news_ct, codename="view_news")
        reader_group.permissions.set([view_perm])

        self.stdout.write(
            self.style.SUCCESS("Groups and permissions created successfully.")
        )
