from django.contrib import admin

from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "relationship", "phone_number", "employee", "is_active")
    list_filter = ("relationship", "is_active")
    search_fields = ("name", "phone_number", "employee__first_name", "employee__last_name")
    ordering = ("employee__last_name", "name")
    raw_id_fields = ("employee",)
