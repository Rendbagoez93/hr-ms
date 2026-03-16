import structlog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .constants import LeaveStatus
from .forms import AttendanceRecordForm, LeaveRequestForm, WorkScheduleForm
from .models import AttendanceRecord, LeaveRequest, WorkSchedule
from .selectors import (
    get_attendance_list,
    get_attendance_record,
    get_leave_request,
    get_leave_request_list,
    get_work_schedule,
    get_work_schedule_list,
)
from .services import (
    approve_leave_request,
    cancel_leave_request,
    create_attendance_record,
    create_leave_request,
    create_work_schedule,
    delete_attendance_record,
    reject_leave_request,
    update_attendance_record,
    update_work_schedule,
)


logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Attendance record views
# ---------------------------------------------------------------------------


class AttendanceListView(LoginRequiredMixin, ListView):
    template_name = "attendance/attendance_list.html"
    context_object_name = "records"
    paginate_by = 25

    def get_queryset(self):
        qs = get_attendance_list()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(employee__first_name__icontains=q) | Q(employee__last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def form_valid(self, form):
        data = form.cleaned_data
        create_attendance_record(
            employee=data["employee"],
            date=data["date"],
            status=data["status"],
            check_in=data.get("check_in"),
            check_out=data.get("check_out"),
            late_minutes=data.get("late_minutes", 0),
            notes=data.get("notes", ""),
        )
        messages.success(self.request, "Attendance record created successfully.")
        return redirect(self.success_url)


class AttendanceDetailView(LoginRequiredMixin, DetailView):
    template_name = "attendance/attendance_detail.html"
    context_object_name = "record"

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])

    def form_valid(self, form):
        data = form.cleaned_data
        update_attendance_record(
            self.object.pk,
            status=data.get("status"),
            check_in=data.get("check_in"),
            check_out=data.get("check_out"),
            late_minutes=data.get("late_minutes"),
            notes=data.get("notes"),
        )
        messages.success(self.request, "Attendance record updated successfully.")
        return redirect(self.success_url)


class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = AttendanceRecord
    template_name = "attendance/attendance_confirm_delete.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])

    def form_valid(self, form):
        delete_attendance_record(self.object.pk)
        messages.success(self.request, "Attendance record deleted.")
        return redirect(self.success_url)


# ---------------------------------------------------------------------------
# Leave request views
# ---------------------------------------------------------------------------


class LeaveRequestListView(LoginRequiredMixin, ListView):
    template_name = "attendance/leave_list.html"
    context_object_name = "leave_requests"
    paginate_by = 25

    def get_queryset(self):
        qs = get_leave_request_list()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(employee__first_name__icontains=q) | Q(employee__last_name__icontains=q)
            )
        status_filter = self.request.GET.get("status", "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_query"] = self.request.GET.get("q", "")
        ctx["status_filter"] = self.request.GET.get("status", "")
        ctx["leave_statuses"] = LeaveStatus.choices()
        return ctx


class LeaveRequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = "attendance/leave_form.html"
    success_url = reverse_lazy("attendance:leave-list")

    def form_valid(self, form):
        data = form.cleaned_data
        create_leave_request(
            employee=data["employee"],
            leave_type=data["leave_type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            reason=data["reason"],
        )
        messages.success(self.request, "Leave request submitted successfully.")
        return redirect(self.success_url)


class LeaveRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "attendance/leave_detail.html"
    context_object_name = "leave_request"

    def get_object(self, queryset=None):
        return get_leave_request(self.kwargs["pk"])


class LeaveApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reviewer_employee = getattr(request.user, "employee_profile", None)
        notes = request.POST.get("notes", "")
        approve_leave_request(pk, reviewed_by=reviewer_employee, notes=notes)
        messages.success(request, "Leave request approved.")
        return redirect(reverse_lazy("attendance:leave-detail", kwargs={"pk": pk}))


class LeaveRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reviewer_employee = getattr(request.user, "employee_profile", None)
        notes = request.POST.get("notes", "")
        reject_leave_request(pk, reviewed_by=reviewer_employee, notes=notes)
        messages.success(request, "Leave request rejected.")
        return redirect(reverse_lazy("attendance:leave-detail", kwargs={"pk": pk}))


class LeaveCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cancel_leave_request(pk)
        messages.success(request, "Leave request cancelled.")
        return redirect(reverse_lazy("attendance:leave-list"))


# ---------------------------------------------------------------------------
# Work schedule views
# ---------------------------------------------------------------------------


class WorkScheduleListView(LoginRequiredMixin, ListView):
    template_name = "attendance/schedule_list.html"
    context_object_name = "schedules"
    paginate_by = 25

    def get_queryset(self):
        return get_work_schedule_list()


class WorkScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = "attendance/schedule_form.html"
    success_url = reverse_lazy("attendance:schedule-list")

    def form_valid(self, form):
        data = form.cleaned_data
        days = frozenset(day for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday") if data.get(day))
        create_work_schedule(
            employee=data["employee"],
            name=data["name"],
            expected_check_in=data["expected_check_in"],
            expected_check_out=data["expected_check_out"],
            effective_from=data["effective_from"],
            work_days=days,
            effective_to=data.get("effective_to"),
        )
        messages.success(self.request, "Work schedule created successfully.")
        return redirect(self.success_url)


class WorkScheduleDetailView(LoginRequiredMixin, DetailView):
    template_name = "attendance/schedule_detail.html"
    context_object_name = "schedule"

    def get_object(self, queryset=None):
        return get_work_schedule(self.kwargs["pk"])


class WorkScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = "attendance/schedule_form.html"
    success_url = reverse_lazy("attendance:schedule-list")

    def get_object(self, queryset=None):
        return get_work_schedule(self.kwargs["pk"])

    def form_valid(self, form):
        data = form.cleaned_data
        days = frozenset(day for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday") if data.get(day))
        update_work_schedule(
            self.object.pk,
            name=data.get("name"),
            expected_check_in=data.get("expected_check_in"),
            expected_check_out=data.get("expected_check_out"),
            effective_to=data.get("effective_to"),
            work_days=days,
            is_default=data.get("is_default"),
        )
        messages.success(self.request, "Work schedule updated successfully.")
        return redirect(self.success_url)
