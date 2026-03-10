from django.contrib import admin

from .models import EmergencyContact, Employee


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 0
    fields = ("name", "relationship", "phone", "email", "is_primary", "is_active")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "gender", "phone", "is_active", "created_at")
    list_filter = ("is_active", "gender", "country")
    search_fields = ("employee_id", "first_name", "last_name", "national_id")
    ordering = ("last_name", "first_name")
    inlines = [EmergencyContactInline]
    readonly_fields = ("created_at", "updated_at")
