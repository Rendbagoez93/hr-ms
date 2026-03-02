"""
Scenario: An employee leaves the company and their account is soft-deleted.
Covers: SoftDeleteManager, BaseModel.delete(), is_active flag, Django authentication.
"""
import pytest
from django.contrib.auth import authenticate

from modules.user.models import User


# ─── Positive Tests ───────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_deleted_user_has_deleted_at_set(ex_employee):
    ex_employee.delete()
    ex_employee.refresh_from_db()
    assert ex_employee.deleted_at is not None


@pytest.mark.django_db
def test_deleted_user_is_inactive(ex_employee):
    ex_employee.delete()
    ex_employee.refresh_from_db()
    assert ex_employee.is_active is False


@pytest.mark.django_db
def test_deleted_user_preserved_for_audit(ex_employee):
    email = ex_employee.email
    ex_employee.delete()
    assert User.all_objects.filter(email=email).exists()


@pytest.mark.django_db
def test_deleted_user_appears_in_deleted_objects(ex_employee):
    email = ex_employee.email
    ex_employee.delete()
    assert User.deleted_objects.filter(email=email).exists()


@pytest.mark.django_db
def test_deleted_user_cannot_authenticate(ex_employee):
    ex_employee.delete()
    result = authenticate(email=ex_employee.email, password="TestPass123!")
    assert result is None


# ─── Negative Tests ───────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_soft_delete_does_not_remove_from_database(ex_employee):
    count_before = User.all_objects.count()
    ex_employee.delete()
    assert User.all_objects.count() == count_before


@pytest.mark.django_db
def test_active_user_can_authenticate(staff_user):
    result = authenticate(email=staff_user.email, password="TestPass123!")
    assert result is not None
    assert result.pk == staff_user.pk


@pytest.mark.django_db
def test_restored_user_can_authenticate(ex_employee):
    ex_employee.delete()
    ex_employee.restore()
    result = authenticate(email=ex_employee.email, password="TestPass123!")
    assert result is not None
