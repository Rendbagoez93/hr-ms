from rest_framework.permissions import BasePermission

from config.roles import Role


class HasRole(BasePermission):
    """Base permission: grant access if the user holds one of `allowed_roles`."""
    allowed_roles: list[str] = []

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsExecutive(HasRole):
    allowed_roles = Role.executive_roles()


class IsManager(HasRole):
    allowed_roles = Role.management_roles()


class IsHR(HasRole):
    allowed_roles = Role.hr_roles()


class IsFinance(HasRole):
    allowed_roles = Role.finance_roles()


class IsIT(HasRole):
    allowed_roles = Role.it_roles()
