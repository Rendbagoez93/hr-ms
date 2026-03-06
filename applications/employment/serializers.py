from rest_framework import serializers

from .models import EmploymentDetail


class EmploymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentDetail
        fields = (
            "id",
            "employee",
            "department",
            "job_title",
            "work_location",
            "work_location_type",
            "employment_status",
            "start_date",
            "reporting_manager",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class EmploymentDetailReadSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    job_title_name = serializers.CharField(source="job_title.title", read_only=True)
    reporting_manager_name = serializers.CharField(source="reporting_manager.full_name", read_only=True)

    class Meta:
        model = EmploymentDetail
        fields = (
            "id",
            "employee",
            "employee_name",
            "department",
            "department_name",
            "job_title",
            "job_title_name",
            "work_location",
            "work_location_type",
            "employment_status",
            "start_date",
            "reporting_manager",
            "reporting_manager_name",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
