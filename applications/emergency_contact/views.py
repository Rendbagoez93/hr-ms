from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import EmergencyContact
from .serializers import EmergencyContactSerializer


class EmergencyContactViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all().select_related("employee")
