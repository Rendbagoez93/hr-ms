from rest_framework import serializers

from .models import EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = (
            "id",
            "employee",
            "name",
            "relationship",
            "phone_number",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
