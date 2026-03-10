"""
Scenario: A Staff member is promoted to HR_Manager.
Covers: role field update, helper properties (is_hr, is_regular_staff), DB persistence.
"""

import pytest

from config.roles import Role
from modules.user.models import User


# ─── Positive Tests ───────────────────────────────────────────────────────────


@pytest.mark.django_db
def test_promoted_user_is_hr(staff_user):
    staff_user.role = Role.HR_MANAGER
    staff_user.save()
    assert staff_user.is_hr is True


@pytest.mark.django_db
def test_promoted_user_loses_regular_staff_status(staff_user):
    staff_user.role = Role.HR_MANAGER
    staff_user.save()
    assert staff_user.is_regular_staff is False


@pytest.mark.django_db
def test_role_change_is_persisted(staff_user):
    staff_user.role = Role.HR_MANAGER
    staff_user.save()
    refreshed = User.objects.get(pk=staff_user.pk)
    assert refreshed.role == Role.HR_MANAGER


# ─── Negative Tests ───────────────────────────────────────────────────────────


@pytest.mark.django_db
def test_staff_user_is_not_hr(staff_user):
    assert staff_user.is_hr is False


@pytest.mark.django_db
def test_non_hr_role_does_not_grant_hr_access(create_user):
    manager = create_user(email="manager@example.com", role=Role.MANAGER)
    assert manager.is_hr is False


@pytest.mark.django_db
def test_in_memory_change_does_not_persist_without_save(staff_user):
    staff_user.role = Role.HR_MANAGER
    # No save() — role change must NOT appear in DB
    refreshed = User.objects.get(pk=staff_user.pk)
    assert refreshed.role == Role.STAFF
