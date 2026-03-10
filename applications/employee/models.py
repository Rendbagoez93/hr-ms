from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel

from .constants import EmergencyContactRelationship, Gender
from .managers import EmployeeManager


class Employee(BaseModel):
    """Central entity representing an employee with personal and contact information."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
        verbose_name=_("user account"),
    )
    employee_id = models.CharField(_("employee ID"), max_length=20, unique=True)

    # Personal details
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    date_of_birth = models.DateField(_("date of birth"))
    gender = models.CharField(_("gender"), max_length=30, choices=Gender.choices())
    nationality = models.CharField(_("nationality"), max_length=100, blank=True)
    national_id = models.CharField(_("national ID"), max_length=50, blank=True)
    photo = models.ImageField(_("photo"), upload_to="employees/photos/", null=True, blank=True)

    # Contact information
    phone = models.CharField(_("phone"), max_length=30, blank=True)
    personal_email = models.EmailField(_("personal email"), blank=True)

    # Address
    address_line_1 = models.CharField(_("address line 1"), max_length=255, blank=True)
    address_line_2 = models.CharField(_("address line 2"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=100, blank=True)
    state_province = models.CharField(_("state / province"), max_length=100, blank=True)
    postal_code = models.CharField(_("postal code"), max_length=20, blank=True)
    country = models.CharField(_("country"), max_length=100, blank=True)

    objects = EmployeeManager()

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ("last_name", "first_name")

    def __str__(self) -> str:
        return f"{self.employee_id} - {self.full_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class EmergencyContact(BaseModel):
    """Emergency contact person for an employee."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
        verbose_name=_("employee"),
    )
    name = models.CharField(_("name"), max_length=200)
    relationship = models.CharField(
        _("relationship"),
        max_length=30,
        choices=EmergencyContactRelationship.choices(),
    )
    phone = models.CharField(_("phone"), max_length=30)
    email = models.EmailField(_("email"), blank=True)
    address = models.TextField(_("address"), blank=True)
    is_primary = models.BooleanField(_("primary contact"), default=False)

    class Meta:
        verbose_name = _("Emergency Contact")
        verbose_name_plural = _("Emergency Contacts")
        ordering = ("-is_primary", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.relationship}) — {self.employee}"
