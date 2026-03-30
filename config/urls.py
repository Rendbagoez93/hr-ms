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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from modules.auth.views import LoginView


urlpatterns = [
    path("", RedirectView.as_view(url="/employees/", permanent=False)),
    path("admin/", admin.site.urls),
    # API
    path("api/auth/", include("modules.auth.urls")),
    # Session auth for template UI (Django built-in)
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    # Template-based UI
    path("org/", include("applications.organization.urls")),
    path("employees/", include("applications.employee.urls")),
    path("employment/", include("applications.employment.urls")),
    path("settings/", include("applications.company_profile.urls")),
    path("attendance/", include("applications.attendance.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

