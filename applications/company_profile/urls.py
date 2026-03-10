from django.urls import include, path

from applications.company_profile import views as company_views


app_name = "settings"

urlpatterns = [
    path("", company_views.SettingsIndexView.as_view(), name="index"),
    path("company/", company_views.CompanyProfileUpdateView.as_view(), name="company-profile"),
    path("imports/", include("applications.imports.urls")),
]
