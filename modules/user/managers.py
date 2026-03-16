from datetime import date
from uuid import uuid4

from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from config.roles import Role


class CustomUserManager(BaseUserManager):
    def _generate_superuser_employee_id(self, *, employee_model):
        while True:
            employee_id = f"EMP-SU-{uuid4().hex[:12].upper()}"
            if not employee_model.all_objects.filter(employee_id=employee_id).exists():
                return employee_id

    def _ensure_superuser_employee_profile(self, *, user):
        if not user.is_superuser:
            return

        employee_model = apps.get_model("employee", "Employee")
        existing_employee = employee_model.all_objects.filter(user=user).first()
        if existing_employee:
            if existing_employee.deleted_at is not None:
                existing_employee.restore()
            return

        first_name = user.first_name.strip() or "System"
        last_name = user.last_name.strip() or "Administrator"

        employee_model.objects.create(
            user=user,
            employee_id=self._generate_superuser_employee_id(employee_model=employee_model),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date(1970, 1, 1),
            gender="prefer_not_to_say",
            personal_email=user.email,
        )

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", Role.ADMINISTRATOR)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        with transaction.atomic():
            user = self.create_user(email, password, **extra_fields)
            self._ensure_superuser_employee_profile(user=user)
            return user
