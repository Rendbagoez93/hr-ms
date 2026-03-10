from django.contrib import admin

from .models import Contract, Employment, Salary


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    fields = ("contract_type", "start_date", "end_date", "is_active")


class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0
    fields = ("pay_grade", "amount", "currency", "payment_frequency", "effective_date", "end_date")


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ("employee", "job_title", "department", "status", "work_location", "hire_date", "is_active")
    list_filter = ("status", "work_location", "department", "is_active")
    search_fields = ("employee__employee_id", "employee__first_name", "employee__last_name")
    ordering = ("-hire_date",)
    inlines = [ContractInline, SalaryInline]
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["employee", "department", "job_title", "reporting_manager"]
