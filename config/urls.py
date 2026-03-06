"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("modules.auth.urls")),
    path("api/departments/", include("applications.department.urls")),
    path("api/job-titles/", include("applications.job_title.urls")),
    path("api/employees/", include("applications.employee.urls")),
    path("api/employments/", include("applications.employment.urls")),
    path("api/contracts/", include("applications.contract.urls")),
    path("api/salaries/", include("applications.salary.urls")),
    path("api/emergency-contacts/", include("applications.emergency_contact.urls")),
]
