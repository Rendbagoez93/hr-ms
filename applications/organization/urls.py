from django.urls import path

from .views import (
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentDetailView,
    DepartmentListView,
    DepartmentUpdateView,
    JobTitleCreateView,
    JobTitleDeleteView,
    JobTitleListView,
    JobTitleUpdateView,
)


app_name = "organization"

urlpatterns = [
    # Departments
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("departments/new/", DepartmentCreateView.as_view(), name="department-create"),
    path("departments/<uuid:pk>/", DepartmentDetailView.as_view(), name="department-detail"),
    path("departments/<uuid:pk>/edit/", DepartmentUpdateView.as_view(), name="department-update"),
    path("departments/<uuid:pk>/delete/", DepartmentDeleteView.as_view(), name="department-delete"),
    # Job Titles
    path("job-titles/", JobTitleListView.as_view(), name="jobtitle-list"),
    path("job-titles/new/", JobTitleCreateView.as_view(), name="jobtitle-create"),
    path("job-titles/<uuid:pk>/edit/", JobTitleUpdateView.as_view(), name="jobtitle-update"),
    path("job-titles/<uuid:pk>/delete/", JobTitleDeleteView.as_view(), name="jobtitle-delete"),
]
