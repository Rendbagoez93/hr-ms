from django import forms

from .models import AttendanceRecord, LeaveRequest, WorkSchedule


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ["employee", "date", "status", "check_in", "check_out", "late_minutes", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "check_in": forms.TimeInput(attrs={"type": "time"}),
            "check_out": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out time must be later than check-in time.")
        return cleaned_data


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["employee", "leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and end < start:
            raise forms.ValidationError("End date must be on or after start date.")
        return cleaned_data


class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = [
            "employee",
            "name",
            "is_default",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "expected_check_in",
            "expected_check_out",
            "effective_from",
            "effective_to",
        ]
        widgets = {
            "expected_check_in": forms.TimeInput(attrs={"type": "time"}),
            "expected_check_out": forms.TimeInput(attrs={"type": "time"}),
            "effective_from": forms.DateInput(attrs={"type": "date"}),
            "effective_to": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("expected_check_in")
        check_out = cleaned_data.get("expected_check_out")
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Expected check-out must be later than expected check-in.")
        effective_from = cleaned_data.get("effective_from")
        effective_to = cleaned_data.get("effective_to")
        if effective_from and effective_to and effective_to < effective_from:
            raise forms.ValidationError("Effective-to date must be on or after effective-from date.")
        return cleaned_data
