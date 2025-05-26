from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("editor", "Editor"),
        ("reader", "Reader"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    plan = models.ForeignKey("Plan", on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username


class Vertical(models.Model):
    VERTICAL_CHOICES = (
        ("poder", "Poder"),
        ("tributos", "Tributos"),
        ("saude", "Saúde"),
        ("energia", "Energia"),
        ("trabalhista", "Trabalhista"),
    )

    name = models.CharField(max_length=50, choices=VERTICAL_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Plan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    verticals = models.ManyToManyField("Vertical", blank=True)
    is_pro = models.BooleanField(default=False)

    def __str__(self):
        return self.name
