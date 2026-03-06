from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.active()
