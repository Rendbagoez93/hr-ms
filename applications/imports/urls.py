from django.urls import path

from . import views


app_name = "imports"

urlpatterns = [
    path("", views.ImportJobListView.as_view(), name="list"),
    path("new/", views.ImportJobCreateView.as_view(), name="create"),
    path("<uuid:pk>/", views.ImportJobDetailView.as_view(), name="detail"),
    path("<uuid:pk>/mapping/", views.ImportJobMappingView.as_view(), name="mapping"),
    path("<uuid:pk>/process/", views.ImportJobProcessView.as_view(), name="process"),
]
