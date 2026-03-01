import pytest

from config.settings.companyconf import (
    Address,
    Benefits,
    BusinessHours,
    CompanyProfile,
    Contact,
    Department,
    HRSettings,
    JobLevel,
    LeavePolicy,
    WorkdayHours,
    Weekdays,
    load_company_config,
)


pytestmark = pytest.mark.unit


# ─── load_company_config ──────────────────────────────────────────────────────

def test_load_returns_company_profile():
    profile = load_company_config()
    assert isinstance(profile, CompanyProfile)


def test_loaded_company_name(company_config):
    assert company_config.name == "Acme Corporation"


def test_loaded_company_has_contact(company_config):
    assert company_config.contact.email == "info@acmecorp.co.id"
    assert company_config.contact.phone.startswith("+62")


def test_loaded_company_address_country(company_config):
    assert company_config.address.country == "Indonesia"


def test_loaded_hr_settings_working_hours(company_config):
    assert company_config.hr_settings.working_hours_per_week == 40


def test_loaded_hr_settings_payroll_cycle(company_config):
    assert company_config.hr_settings.payroll_cycle == "monthly"


def test_loaded_leave_policies_count(company_config):
    assert len(company_config.leave_policies) == 6


def test_annual_leave_carry_over(company_config):
    annual = next(p for p in company_config.leave_policies if p.type == "annual")
    assert annual.carry_over is True
    assert annual.max_carry_over_days == 6


def test_sick_leave_no_carry_over(company_config):
    sick = next(p for p in company_config.leave_policies if p.type == "sick")
    assert sick.carry_over is False
    assert sick.max_carry_over_days == 0


def test_job_levels_are_ordered(company_config):
    levels = [jl.level for jl in company_config.job_levels]
    assert levels == sorted(levels)


def test_business_hours_timezone(company_config):
    assert company_config.business_hours.timezone == "Asia/Jakarta"


def test_departments_count(company_config):
    assert len(company_config.departments) == 9


def test_department_codes_are_unique(company_config):
    codes = [d.code for d in company_config.departments]
    assert len(codes) == len(set(codes))


# ─── Pydantic model validation ────────────────────────────────────────────────

def test_company_profile_requires_name():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        CompanyProfile(
            contact=Contact(email="a@b.com", phone="123"),
            address=Address(street="x", city="x", country="x"),
            hr_settings=HRSettings(
                working_hours_per_week=40,
                default_currency="IDR",
                payroll_cycle="monthly",
            ),
        )


def test_minimal_company_profile_is_valid():
    profile = CompanyProfile(
        name="Test Co",
        contact=Contact(email="hr@test.com", phone="+1-800-000-0000"),
        address=Address(street="1 Main St", city="Jakarta", country="Indonesia"),
        hr_settings=HRSettings(
            working_hours_per_week=40,
            default_currency="IDR",
            payroll_cycle="monthly",
        ),
    )
    assert profile.name == "Test Co"
    assert profile.leave_policies == []
    assert profile.departments == []


def test_leave_policy_model_fields():
    policy = LeavePolicy(type="annual", label="Annual Leave", days=12, carry_over=True, max_carry_over_days=6)
    assert policy.days == 12
    assert policy.carry_over is True


def test_job_level_model_fields():
    jl = JobLevel(level=3, code="SR", label="Senior")
    assert jl.code == "SR"


def test_benefits_defaults_to_false():
    b = Benefits()
    assert b.health_insurance is False
    assert b.annual_bonus is False


def test_workday_hours_model():
    wd = WorkdayHours(start="09:00", end="17:00")
    assert wd.start == "09:00"


def test_business_hours_defaults_to_utc():
    bh = BusinessHours()
    assert bh.timezone == "UTC"


def test_weekdays_all_optional():
    wd = Weekdays()
    assert wd.monday is None


def test_department_model_fields():
    dept = Department(name="Engineering", code="ENG")
    assert dept.code == "ENG"
