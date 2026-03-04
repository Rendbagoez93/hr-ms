from unittest.mock import Mock

import pytest

from modules.auth.permissions import IsExecutive, IsFinance, IsHR, IsIT, IsManager


def _request_for(user):
    req = Mock()
    req.user = user
    return req


@pytest.mark.django_db
class TestHasRolePermissions:
    def test_executive_grants_executive_role(self, executive_user):
        assert IsExecutive().has_permission(_request_for(executive_user), None) is True

    def test_executive_denies_staff_role(self, staff_user):
        assert IsExecutive().has_permission(_request_for(staff_user), None) is False

    def test_manager_grants_manager_role(self, manager_user):
        assert IsManager().has_permission(_request_for(manager_user), None) is True

    def test_manager_denies_staff_role(self, staff_user):
        assert IsManager().has_permission(_request_for(staff_user), None) is False

    def test_hr_grants_hr_role(self, hr_user):
        assert IsHR().has_permission(_request_for(hr_user), None) is True

    def test_hr_denies_staff_role(self, staff_user):
        assert IsHR().has_permission(_request_for(staff_user), None) is False

    def test_finance_grants_finance_role(self, finance_user):
        assert IsFinance().has_permission(_request_for(finance_user), None) is True

    def test_it_grants_it_role(self, it_user):
        assert IsIT().has_permission(_request_for(it_user), None) is True

    def test_unauthenticated_is_denied(self):
        req = Mock()
        req.user = Mock(is_authenticated=False)
        assert IsExecutive().has_permission(req, None) is False
