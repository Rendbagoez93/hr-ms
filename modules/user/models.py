from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.roles import Role
from shared.base_models import BaseModel

from .managers import CustomUserManager


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.STAFF,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def is_executive(self):
        return self.role in Role.executive_roles()

    @property
    def is_manager(self):
        return self.role in Role.management_roles()

    @property
    def is_hr(self):
        return self.role in Role.hr_roles()

    @property
    def is_finance(self):
        return self.role in Role.finance_roles()

    @property
    def is_it(self):
        return self.role in Role.it_roles()

    @property
    def is_operations(self):
        return self.role in Role.operations_roles()

    @property
    def is_safety_security(self):
        return self.role in Role.safety_and_security_roles()

    @property
    def is_regular_staff(self):
        return self.role in Role.regular_roles()
