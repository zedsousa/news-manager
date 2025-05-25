from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("editor", "Editor"),
        ("reader", "Reader"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    plan = models.ForeignKey("Plan", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class Vertical(models.Model):
    VERTICAL_CHOICES = (
        ("power", "Power"),
        ("taxes", "Taxes"),
        ("health", "Health"),
        ("energy", "Energy"),
        ("labor", "Labor"),
    )

    name = models.CharField(max_length=10, choices=VERTICAL_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Plan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    verticals = models.ManyToManyField("Vertical", blank=True)
    is_pro = models.BooleanField(default=False)

    def generate_name(self):
        if self.is_pro:
            vertical_names = sorted([str(v) for v in self.verticals.all()])
            return f"JOTA PRO {' + '.join(vertical_names)}"
        return "JOTA Info"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.name = self.generate_name()
            super().save(update_fields=["name"])
