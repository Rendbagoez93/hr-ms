from django.contrib import admin

from .models import Salary


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("employee", "amount", "currency", "frequency", "pay_grade", "effective_date", "is_active")
    list_filter = ("frequency", "currency", "is_active")
    search_fields = ("employee__first_name", "employee__last_name", "pay_grade")
    ordering = ("-effective_date",)
    raw_id_fields = ("employee",)
