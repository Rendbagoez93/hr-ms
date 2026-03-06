from rest_framework.routers import DefaultRouter

from .views import JobTitleViewSet

router = DefaultRouter()
router.register("", JobTitleViewSet, basename="job-title")

urlpatterns = router.urls
