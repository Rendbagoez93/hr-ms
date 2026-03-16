from django import forms

from .models import Contract, Employment, Salary


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = (
            "employee", "department", "job_title", "reporting_manager",
            "work_location", "status", "hire_date", "end_date",
        )
        widgets = {  # noqa: RUF012
            "hire_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class EmploymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ("department", "job_title", "reporting_manager", "work_location", "status", "hire_date", "end_date")
        widgets = {  # noqa: RUF012
            "hire_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("contract_type", "start_date", "end_date", "terms", "document")
        widgets = {  # noqa: RUF012
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ("pay_grade", "amount", "currency", "payment_frequency", "effective_date", "end_date", "notes")
        widgets = {  # noqa: RUF012
            "effective_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
