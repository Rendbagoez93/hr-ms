from django.contrib import admin

from .models import JobTitle


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("title",)
