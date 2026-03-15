from django.urls import path

from .views import (
    AttendanceCreateView,
    AttendanceDeleteView,
    AttendanceDetailView,
    AttendanceListView,
    AttendanceUpdateView,
    LeaveApproveView,
    LeaveCancelView,
    LeaveRejectView,
    LeaveRequestCreateView,
    LeaveRequestDetailView,
    LeaveRequestListView,
    WorkScheduleCreateView,
    WorkScheduleDetailView,
    WorkScheduleListView,
    WorkScheduleUpdateView,
)


app_name = "attendance"

urlpatterns = [
    # Attendance records
    path("", AttendanceListView.as_view(), name="attendance-list"),
    path("new/", AttendanceCreateView.as_view(), name="attendance-create"),
    path("<uuid:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"),
    path("<uuid:pk>/edit/", AttendanceUpdateView.as_view(), name="attendance-update"),
    path("<uuid:pk>/delete/", AttendanceDeleteView.as_view(), name="attendance-delete"),
    # Leave requests
    path("leave/", LeaveRequestListView.as_view(), name="leave-list"),
    path("leave/new/", LeaveRequestCreateView.as_view(), name="leave-create"),
    path("leave/<uuid:pk>/", LeaveRequestDetailView.as_view(), name="leave-detail"),
    path("leave/<uuid:pk>/approve/", LeaveApproveView.as_view(), name="leave-approve"),
    path("leave/<uuid:pk>/reject/", LeaveRejectView.as_view(), name="leave-reject"),
    path("leave/<uuid:pk>/cancel/", LeaveCancelView.as_view(), name="leave-cancel"),
    # Work schedules
    path("schedules/", WorkScheduleListView.as_view(), name="schedule-list"),
    path("schedules/new/", WorkScheduleCreateView.as_view(), name="schedule-create"),
    path("schedules/<uuid:pk>/", WorkScheduleDetailView.as_view(), name="schedule-detail"),
    path("schedules/<uuid:pk>/edit/", WorkScheduleUpdateView.as_view(), name="schedule-update"),
]
