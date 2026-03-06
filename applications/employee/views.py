from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeListSerializer, EmployeeSerializer


class EmployeeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.active().with_employment()

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer
