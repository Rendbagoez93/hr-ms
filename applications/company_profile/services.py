"""
Services for CompanyProfile — singleton access and YAML seed.
"""

from __future__ import annotations

from typing import Any

import structlog

from .models import CompanyProfile


logger = structlog.get_logger(__name__)


def get_or_create_company_profile() -> CompanyProfile:
    """Return the active company profile, creating an empty one if none exists."""
    profile = CompanyProfile.objects.filter(is_active=True).first()
    if profile is None:
        profile = CompanyProfile.objects.create(name="Your Company")
        logger.info("Created empty CompanyProfile")
    return profile


def seed_from_yaml(company_config: Any) -> CompanyProfile:
    """
    Populate (or update) the CompanyProfile from the loaded company_config.yaml object.
    Safe to call multiple times — it is idempotent.
    """
    profile = CompanyProfile.objects.filter(is_active=True).first()

    contact = getattr(company_config, "contact", None)
    address = getattr(company_config, "address", None)
    social = getattr(contact, "social_media", None) if contact else None
    hr = getattr(company_config, "hr_settings", None)
    bh = getattr(company_config, "business_hours", None)

    data: dict[str, Any] = {
        "name": getattr(company_config, "name", ""),
        "legal_name": getattr(company_config, "legal_name", ""),
        "tax_id": getattr(company_config, "tax_id", ""),
        "registration_number": getattr(company_config, "registration_number", ""),
        "industry": getattr(company_config, "industry", ""),
        "founded": str(getattr(company_config, "founded", "")),
        "email": getattr(contact, "email", "") if contact else "",
        "phone": getattr(contact, "phone", "") if contact else "",
        "website": getattr(contact, "website", "") if contact else "",
        "linkedin": getattr(social, "linkedin", "") if social else "",
        "instagram": getattr(social, "instagram", "") if social else "",
        "twitter": getattr(social, "twitter", "") if social else "",
        "address_street": getattr(address, "street", "") if address else "",
        "address_city": getattr(address, "city", "") if address else "",
        "address_state": getattr(address, "state", "") if address else "",
        "address_postal_code": getattr(address, "postal_code", "") if address else "",
        "address_country": getattr(address, "country", "") if address else "",
        "work_hours_per_week": getattr(hr, "work_hours_per_week", 40) if hr else 40,
        "probation_days": getattr(hr, "probation_period_days", 90) if hr else 90,
        "annual_leave_days": getattr(hr, "annual_leave_days", 12) if hr else 12,
        "sick_leave_days": getattr(hr, "sick_leave_days", 12) if hr else 12,
        "default_currency": getattr(hr, "default_currency", "IDR") if hr else "IDR",
        "payroll_cycle": getattr(hr, "payroll_cycle", "monthly") if hr else "monthly",
        "employee_id_format": getattr(hr, "employee_id_format", "EMP-{YEAR}-{SEQ:04d}") if hr else "EMP-{YEAR}-{SEQ:04d}",
        "timezone": getattr(bh, "timezone", "Asia/Jakarta") if bh else "Asia/Jakarta",
    }

    if profile is None:
        profile = CompanyProfile.objects.create(**data)
        logger.info("Seeded CompanyProfile from YAML", name=data["name"])
    else:
        for field, value in data.items():
            setattr(profile, field, value)
        profile.save()
        logger.info("Updated CompanyProfile from YAML", name=data["name"])

    return profile


def update_company_profile(profile: CompanyProfile, cleaned_data: dict[str, Any]) -> CompanyProfile:
    """Apply form-cleaned data to the profile and save."""
    for field, value in cleaned_data.items():
        setattr(profile, field, value)
    profile.save()
    logger.info("CompanyProfile updated", pk=str(profile.pk))
    return profile
