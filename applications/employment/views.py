from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import EmploymentDetail
from .serializers import EmploymentDetailReadSerializer, EmploymentDetailSerializer


class EmploymentDetailViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = EmploymentDetail.objects.active().with_relations()

    def get_serializer_class(self):
        if self.action in {"list", "retrieve"}:
            return EmploymentDetailReadSerializer
        return EmploymentDetailSerializer
