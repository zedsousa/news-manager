from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Plan, User, Vertical


@receiver(post_save, sender=User)
def assign_default_plan(sender, instance, created, **kwargs):
    if created and instance.plan is None:
        default_plan, _ = Plan.objects.get_or_create(name="JOTA Info", is_pro=False)
        instance.plan = default_plan
        instance.save()


@receiver(post_migrate)
def create_default_verticals(sender, **kwargs):
    for code, _ in Vertical.VERTICAL_CHOICES:
        Vertical.objects.get_or_create(name=code)
