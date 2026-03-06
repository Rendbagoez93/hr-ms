from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .serializers import ContractSerializer


class ContractViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer
    queryset = Contract.objects.active().select_related("employee")
