"""
Company profile configuration from YAML file.
Loads company-specific settings using Pydantic models.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class ContactInfo(BaseModel):
    """Company contact information."""

    email: str = Field(..., description="Company email address")
    phone: str = Field(..., description="Company phone number")
    website: str = Field(..., description="Company website URL")


class Address(BaseModel):
    """Company physical address."""

    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State or province")
    postal_code: str = Field(..., description="Postal code")
    country: str = Field(..., description="Country")

    def format_full_address(self) -> str:
        """Format complete address as a single string."""
        return (
            f"{self.street}, {self.city}, "
            f"{self.state} {self.postal_code}, {self.country}"
        )


class HRSettings(BaseModel):
    """HR-specific company settings."""

    working_hours_per_week: int = Field(
        ..., ge=1, le=168, description="Standard working hours per week"
    )
    probation_period_days: int = Field(
        ..., ge=0, description="Probation period in days"
    )
    annual_leave_days: int = Field(..., ge=0, description="Annual leave days")
    sick_leave_days: int = Field(..., ge=0, description="Sick leave days")
    default_currency: str = Field(..., description="Default currency code")
    payroll_cycle: str = Field(..., description="Payroll processing cycle")

    @field_validator("payroll_cycle")
    @classmethod
    def validate_payroll_cycle(cls, v: str) -> str:
        """Validate payroll cycle options."""
        valid_cycles = ["weekly", "biweekly", "monthly", "semi-monthly"]
        if v.lower() not in valid_cycles:
            raise ValueError(
                f"Payroll cycle must be one of: {', '.join(valid_cycles)}"
            )
        return v.lower()


class WorkingHours(BaseModel):
    """Working hours for a specific day."""

    start: str | None = Field(None, description="Start time (HH:MM format)")
    end: str | None = Field(None, description="End time (HH:MM format)")

    @field_validator("start", "end")
    @classmethod
    def validate_time_format(cls, v: str | None) -> str | None:
        """Validate time format."""
        if v is None:
            return v
        try:
            hours, minutes = map(int, v.split(":"))
            if not (0 <= hours < 24 and 0 <= minutes < 60):
                raise ValueError
            return v
        except (ValueError, AttributeError):
            raise ValueError("Time must be in HH:MM format")

    @property
    def is_working_day(self) -> bool:
        """Check if this is a working day."""
        return self.start is not None and self.end is not None


class Weekdays(BaseModel):
    """Weekday working hours."""

    monday: WorkingHours
    tuesday: WorkingHours
    wednesday: WorkingHours
    thursday: WorkingHours
    friday: WorkingHours


class Weekend(BaseModel):
    """Weekend working hours."""

    saturday: WorkingHours | None = None
    sunday: WorkingHours | None = None


class BusinessHours(BaseModel):
    """Company business hours configuration."""

    timezone: str = Field(..., description="Company timezone")
    weekdays: Weekdays
    weekend: Weekend


class Department(BaseModel):
    """Department information."""

    name: str = Field(..., description="Department name")
    code: str = Field(..., description="Department code")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate department code format."""
        return v.upper()


class CompanyProfile(BaseModel):
    """Complete company profile model."""

    name: str = Field(..., description="Company name")
    legal_name: str = Field(..., description="Legal company name")
    description: str = Field(..., description="Company description")
    industry: str = Field(..., description="Industry sector")
    founded: int = Field(..., ge=1800, le=2100, description="Year founded")
    tax_id: str = Field(..., description="Tax identification number")
    contact: ContactInfo
    address: Address
    hr_settings: HRSettings
    business_hours: BusinessHours
    departments: list[Department]

    @field_validator("departments")
    @classmethod
    def validate_departments(cls, v: list[Department]) -> list[Department]:
        """Ensure unique department codes."""
        codes = [dept.code for dept in v]
        if len(codes) != len(set(codes)):
            raise ValueError("Department codes must be unique")
        return v

    def get_department_by_code(self, code: str) -> Department | None:
        """Find department by code."""
        code = code.upper()
        for dept in self.departments:
            if dept.code == code:
                return dept
        return None

    def get_department_codes(self) -> list[str]:
        """Get list of all department codes."""
        return [dept.code for dept in self.departments]


class CompanySettings(YamlBaseSettings):
    """Company settings loaded from YAML file."""

    model_config = SettingsConfigDict(
        yaml_file="comp-profile.yaml",
        yaml_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    company: CompanyProfile

    @classmethod
    def from_yaml(cls, yaml_file: str | Path | None = None) -> "CompanySettings":
        """
        Load company settings from YAML file.

        Args:
            yaml_file: Path to YAML file. Uses default if not provided.

        Returns:
            CompanySettings: Loaded company settings.
        """
        if yaml_file is None:
            return cls()

        # Update config with custom file path
        updated_config = cls.model_config.copy()
        updated_config["yaml_file"] = str(yaml_file)

        class CustomCompanySettings(YamlBaseSettings):
            model_config = updated_config
            company: CompanyProfile

        return CustomCompanySettings()

    def to_dict(self) -> dict[str, Any]:
        """Convert company settings to dictionary."""
        return self.company.model_dump()

    def get_company_context(self) -> dict[str, Any]:
        """
        Get company context for Django templates.

        Returns:
            dict: Company information for template context.
        """
        return {
            "company_name": self.company.name,
            "company_legal_name": self.company.legal_name,
            "company_description": self.company.description,
            "company_email": self.company.contact.email,
            "company_phone": self.company.contact.phone,
            "company_website": self.company.contact.website,
            "company_address": self.company.address.format_full_address(),
            "company_timezone": self.company.business_hours.timezone,
            "company_currency": self.company.hr_settings.default_currency,
        }


def get_company_settings(yaml_file: str | Path | None = None) -> CompanySettings:
    """
    Factory function to get company settings.

    Args:
        yaml_file: Optional custom YAML file path.

    Returns:
        CompanySettings: Loaded company settings instance.

    Example:
        >>> settings = get_company_settings()
        >>> print(settings.company.name)
        'Acme Corporation'
    """
    return CompanySettings.from_yaml(yaml_file)
