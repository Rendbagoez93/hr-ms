from django.contrib import admin

from .models import AttendanceRecord, LeaveRequest, WorkSchedule


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ("employee", "name", "is_default", "expected_check_in", "expected_check_out", "effective_from", "effective_to", "is_active")
    list_filter = ("is_default", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    search_fields = ("employee__first_name", "employee__last_name", "employee__employee_id", "name")
    ordering = ("employee__last_name", "-effective_from")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status", "check_in", "check_out", "work_hours", "late_minutes", "is_active", "created_at")
    list_filter = ("status", "is_active", "date")
    search_fields = ("employee__first_name", "employee__last_name", "employee__employee_id")
    ordering = ("-date",)
    readonly_fields = ("created_at", "updated_at", "work_hours")
    date_hierarchy = "date"


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "leave_type", "start_date", "end_date", "total_days", "status", "approved_by", "reviewed_at")
    list_filter = ("status", "leave_type")
    search_fields = ("employee__first_name", "employee__last_name", "employee__employee_id")
    ordering = ("-start_date",)
    readonly_fields = ("created_at", "updated_at", "total_days", "reviewed_at")
