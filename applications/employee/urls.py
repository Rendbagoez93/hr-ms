from django.urls import path

from .views import (
    EmergencyContactCreateView,
    EmergencyContactDeleteView,
    EmergencyContactUpdateView,
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
)


app_name = "employee"

urlpatterns = [
    # Employees
    path("", EmployeeListView.as_view(), name="employee-list"),
    path("new/", EmployeeCreateView.as_view(), name="employee-create"),
    path("<uuid:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("<uuid:pk>/edit/", EmployeeUpdateView.as_view(), name="employee-update"),
    path("<uuid:pk>/delete/", EmployeeDeleteView.as_view(), name="employee-delete"),
    # Emergency contacts (nested under employee)
    path("<uuid:pk>/emergency-contacts/new/", EmergencyContactCreateView.as_view(), name="ec-create"),
    path("<uuid:pk>/emergency-contacts/<uuid:ec_pk>/edit/", EmergencyContactUpdateView.as_view(), name="ec-update"),
    path("<uuid:pk>/emergency-contacts/<uuid:ec_pk>/delete/", EmergencyContactDeleteView.as_view(), name="ec-delete"),
]
