from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource


_BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Sub-models (mirror company_config.yaml structure)
# ---------------------------------------------------------------------------


class SocialMedia(BaseModel):
    linkedin: str | None = None
    instagram: str | None = None
    twitter: str | None = None


class Contact(BaseModel):
    email: str
    phone: str
    website: str | None = None
    social_media: SocialMedia | None = None


class Address(BaseModel):
    street: str
    city: str
    state: str | None = None
    postal_code: str | None = None
    country: str


class HRSettings(BaseModel):
    working_hours_per_week: float
    probation_period_days: int = 90
    annual_leave_days: int = 12
    sick_leave_days: int = 12
    default_currency: str
    payroll_cycle: str
    employee_id_format: str = "EMP-{YEAR}-{SEQ:04d}"


class LeavePolicy(BaseModel):
    type: str
    label: str
    days: int
    carry_over: bool
    max_carry_over_days: int


class JobLevel(BaseModel):
    level: int
    code: str
    label: str


class Benefits(BaseModel):
    health_insurance: bool = False
    dental_insurance: bool = False
    vision_insurance: bool = False
    life_insurance: bool = False
    meal_allowance: bool = False
    transportation_allowance: bool = False
    remote_work_allowance: bool = False
    annual_bonus: bool = False
    performance_bonus: bool = False


class WorkdayHours(BaseModel):
    start: str
    end: str


class Weekdays(BaseModel):
    monday: WorkdayHours | None = None
    tuesday: WorkdayHours | None = None
    wednesday: WorkdayHours | None = None
    thursday: WorkdayHours | None = None
    friday: WorkdayHours | None = None


class Weekend(BaseModel):
    saturday: WorkdayHours | None = None
    sunday: WorkdayHours | None = None


class BusinessHours(BaseModel):
    timezone: str = "UTC"
    weekdays: Weekdays | None = None
    weekend: Weekend | None = None


class Department(BaseModel):
    name: str
    code: str


class CompanyProfile(BaseModel):
    name: str
    legal_name: str | None = None
    description: str | None = None
    industry: str | None = None
    founded: int | None = None
    tax_id: str | None = None
    registration_number: str | None = None
    contact: Contact
    address: Address
    hr_settings: HRSettings
    leave_policies: list[LeavePolicy] = []
    job_levels: list[JobLevel] = []
    benefits: Benefits = Benefits()
    business_hours: BusinessHours = BusinessHours()
    departments: list[Department] = []


# ---------------------------------------------------------------------------
# Root YAML loader
# ---------------------------------------------------------------------------


class CompanyConfig(BaseSettings):
    company: CompanyProfile

    model_config = SettingsConfigDict(
        yaml_file=str(_BASE_DIR / "company_config.yaml"),
        secrets_dir=None,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(cls, settings_cls, **_kwargs):
        return (YamlConfigSettingsSource(settings_cls),)


def load_company_config() -> CompanyProfile:
    return CompanyConfig().company
