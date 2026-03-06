from django.contrib import admin

from .models import EmploymentDetail


@admin.register(EmploymentDetail)
class EmploymentDetailAdmin(admin.ModelAdmin):
    list_display = ("employee", "department", "job_title", "employment_status", "work_location_type", "start_date", "is_active")
    list_filter = ("employment_status", "work_location_type", "is_active", "department")
    search_fields = ("employee__first_name", "employee__last_name", "work_location")
    ordering = ("employee__last_name",)
    raw_id_fields = ("employee", "department", "job_title", "reporting_manager")
