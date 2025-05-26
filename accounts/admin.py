from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Plan, User, Vertical


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "email", "role", "plan", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "plan")
    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("role", "plan")}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "plan")}),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "is_pro")
    filter_horizontal = ("verticals",)


@admin.register(Vertical)
class VerticalAdmin(admin.ModelAdmin):
    list_display = ("name",)
