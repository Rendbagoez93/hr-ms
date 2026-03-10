from django.urls import path

from .views import (
    ContractCreateView,
    ContractDeleteView,
    ContractUpdateView,
    EmploymentCreateView,
    EmploymentDetailView,
    EmploymentListView,
    EmploymentUpdateView,
    SalaryCreateView,
    SalaryDeleteView,
    SalaryUpdateView,
)


app_name = "employment"

urlpatterns = [
    # Employment records
    path("", EmploymentListView.as_view(), name="employment-list"),
    path("new/", EmploymentCreateView.as_view(), name="employment-create"),
    path("<uuid:pk>/", EmploymentDetailView.as_view(), name="employment-detail"),
    path("<uuid:pk>/edit/", EmploymentUpdateView.as_view(), name="employment-update"),
    # Contracts (nested under employment)
    path("<uuid:pk>/contracts/new/", ContractCreateView.as_view(), name="contract-create"),
    path("<uuid:pk>/contracts/<uuid:c_pk>/edit/", ContractUpdateView.as_view(), name="contract-update"),
    path("<uuid:pk>/contracts/<uuid:c_pk>/delete/", ContractDeleteView.as_view(), name="contract-delete"),
    # Salary history (nested under employment)
    path("<uuid:pk>/salary/new/", SalaryCreateView.as_view(), name="salary-create"),
    path("<uuid:pk>/salary/<uuid:s_pk>/edit/", SalaryUpdateView.as_view(), name="salary-update"),
    path("<uuid:pk>/salary/<uuid:s_pk>/delete/", SalaryDeleteView.as_view(), name="salary-delete"),
]
