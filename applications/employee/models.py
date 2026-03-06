from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    OTHER = "other", _("Other")
    PREFER_NOT_TO_SAY = "prefer_not_to_say", _("Prefer Not to Say")


class EmployeeQuerySet(models.QuerySet["Employee"]):
    def active(self) -> "EmployeeQuerySet":
        return self.filter(is_active=True)

    def with_employment(self) -> "EmployeeQuerySet":
        return self.select_related("employment_detail__department", "employment_detail__job_title")


class Employee(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
        verbose_name=_("system user"),
    )
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    date_of_birth = models.DateField(_("date of birth"))
    gender = models.CharField(
        _("gender"),
        max_length=20,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
    )
    address = models.TextField(_("address"), blank=True, default="")
    phone_number = models.CharField(_("phone number"), max_length=20, blank=True, default="")
    photo = models.ImageField(_("photo"), upload_to="employees/photos/", null=True, blank=True)

    objects = EmployeeQuerySet.as_manager()

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
