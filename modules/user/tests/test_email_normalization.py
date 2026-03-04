"""
Scenario: A user registers with Admin@Company.com and tries to log in with admin@company.com.
Covers: CustomUserManager.normalize_email, email uniqueness, case-sensitivity edge cases.

Note: Django's normalize_email lowercases the domain part only (RFC 5321).
      The local part (before @) is preserved as-is, which can allow near-duplicates.
"""
import pytest
from django.db import IntegrityError

from modules.user.models import User


# ─── Positive Tests ───────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_email_domain_is_lowercased_on_creation(db):
    user = User.objects.create_user(email="Admin@COMPANY.COM", password="TestPass123!")
    assert user.email == "Admin@company.com"


@pytest.mark.django_db
def test_normalized_email_is_persisted_to_db(db):
    User.objects.create_user(email="Staff@Example.COM", password="TestPass123!")
    assert User.objects.filter(email="Staff@example.com").exists()


# ─── Negative Tests ───────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_exact_duplicate_email_raises_integrity_error(db):
    User.objects.create_user(email="admin@company.com", password="TestPass123!")
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="admin@company.com", password="AnotherPass!")


@pytest.mark.django_db
def test_missing_email_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="TestPass123!")


@pytest.mark.django_db
def test_local_part_case_creates_distinct_users(db):
    """Exposes limitation: local-part casing is not normalized.
    Admin@company.com and admin@company.com are stored as two separate accounts.
    """
    user_a = User.objects.create_user(email="Admin@company.com", password="TestPass123!")
    user_b = User.objects.create_user(email="admin@company.com", password="TestPass123!")
    assert user_a.pk != user_b.pk
