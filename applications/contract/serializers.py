from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            "id",
            "employee",
            "contract_type",
            "start_date",
            "end_date",
            "terms",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
