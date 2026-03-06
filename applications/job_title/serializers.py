from rest_framework import serializers

from .models import JobTitle


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ("id", "title", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
