from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "full_name",
            "date_of_birth",
            "gender",
            "address",
            "phone_number",
            "photo",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "full_name", "created_at", "updated_at")


class EmployeeListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = ("id", "full_name", "gender", "phone_number", "is_active")
        read_only_fields = fields
