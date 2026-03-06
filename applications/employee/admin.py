from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "gender", "phone_number", "is_active", "created_at")
    list_filter = ("gender", "is_active")
    search_fields = ("first_name", "last_name", "phone_number")
    ordering = ("last_name", "first_name")
    raw_id_fields = ("user",)
