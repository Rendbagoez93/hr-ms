from rest_framework import serializers

from .models import Salary


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = (
            "id",
            "employee",
            "pay_grade",
            "amount",
            "currency",
            "frequency",
            "effective_date",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
