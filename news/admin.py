from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_date")
    list_filter = ("status", "published_date")
    search_fields = ("title", "subtitle", "content", "author__username")
