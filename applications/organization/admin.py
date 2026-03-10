from django.contrib import admin

from .models import Department, JobTitle


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "parent", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "department", "is_active", "created_at")
    list_filter = ("is_active", "department")
    search_fields = ("name", "code")
    ordering = ("name",)
