from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("employee", "contract_type", "start_date", "end_date", "is_active")
    list_filter = ("contract_type", "is_active")
    search_fields = ("employee__first_name", "employee__last_name")
    ordering = ("-start_date",)
    raw_id_fields = ("employee",)
