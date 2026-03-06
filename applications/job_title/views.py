from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import JobTitle
from .serializers import JobTitleSerializer


class JobTitleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = JobTitleSerializer
    queryset = JobTitle.objects.active()
