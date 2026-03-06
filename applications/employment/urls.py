from rest_framework.routers import DefaultRouter

from .views import EmploymentDetailViewSet

router = DefaultRouter()
router.register("", EmploymentDetailViewSet, basename="employment-detail")

urlpatterns = router.urls
