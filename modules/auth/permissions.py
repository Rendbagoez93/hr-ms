from rest_framework.permissions import BasePermission

from config.roles import Role
from modules.auth.constant import ROLE_PERMISSIONS, Permission


# ─────────────────────────────────────────────────────────────────────────────
# Base helpers
# ─────────────────────────────────────────────────────────────────────────────

class HasRole(BasePermission):
    """Grant access when the authenticated user holds one of `allowed_roles`."""

    allowed_roles: list[str] = []

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class HasPermission(BasePermission):
    required_permissions: list[Permission] = []

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        role_perms = ROLE_PERMISSIONS.get(request.user.role, frozenset())
        return all(p in role_perms for p in self.required_permissions)


def make_permission(*permissions: Permission) -> type[HasPermission]:
    return type(
        "DynamicHasPermission",
        (HasPermission,),
        {"required_permissions": list(permissions)},
    )


# ─────────────────────────────────────────────────────────────────────────────
# Role-group permission classes
# ─────────────────────────────────────────────────────────────────────────────

class IsExecutive(HasRole):
    """C-suite, Directors and Vice Presidents."""
    allowed_roles = Role.executive_roles()


class IsManager(HasRole):
    """General Managers, Managers, Supervisors, Team Leads and
    functional Operations / Sales Managers."""
    allowed_roles = Role.management_roles()


class IsHR(HasRole):
    """HR Managers, HR Officers, Recruiters and Payroll Officers."""
    allowed_roles = Role.hr_roles()


class IsFinance(HasRole):
    """CFO, Finance Managers, Accountants, Finance Analysts and Auditors."""
    allowed_roles = Role.finance_roles()


class IsIT(HasRole):
    """Administrators, IT Managers, Developers, System Analysts and IT Support."""
    allowed_roles = Role.it_roles()


class IsAdministrative(HasRole):
    """Office Managers, Executive Assistants, Receptionists and Clerks."""
    allowed_roles = Role.administrative_roles()


class IsSalesOrMarketing(HasRole):
    """Sales Managers, Sales Representatives and Marketing Specialists."""
    allowed_roles = Role.sales_and_marketing_roles()


class IsOperations(HasRole):
    """Operations Managers, Logistics Coordinators and Inventory Controllers."""
    allowed_roles = Role.operations_roles()


class IsSafetyOrSecurity(HasRole):
    """Safety Officers and Security Officers."""
    allowed_roles = Role.safety_and_security_roles()


class IsRegularStaff(HasRole):
    """Staff, Interns, Contractors and Part-time employees."""
    allowed_roles = Role.regular_roles()


# ─────────────────────────────────────────────────────────────────────────────
# Cross-role convenience classes (derived from role group classmethods)
# ─────────────────────────────────────────────────────────────────────────────

class IsPrivileged(HasRole):
    """Executives and IT roles that may bypass standard permission checks."""
    allowed_roles = Role.privileged_roles()


class IsApprover(HasRole):
    """Any role authorised to approve leave, expenses, and overtime requests."""
    allowed_roles = Role.approver_roles()


# ─────────────────────────────────────────────────────────────────────────────
# Fine-grained permission gate classes
#
# Each class is named after the capability it guards and can be used directly
# in `permission_classes` or combined with `|` / `&` operators.
# ─────────────────────────────────────────────────────────────────────────────

# ── Employee management ───────────────────────────────────────────────────────

class CanViewEmployeeList(HasPermission):
    required_permissions = [Permission.VIEW_EMPLOYEE_LIST]


class CanManageEmployees(HasPermission):
    """Create and edit employees (does not cover deletion)."""
    required_permissions = [Permission.CREATE_EMPLOYEE, Permission.EDIT_EMPLOYEE]


class CanDeleteEmployee(HasPermission):
    required_permissions = [Permission.DELETE_EMPLOYEE]


# ── Leave ─────────────────────────────────────────────────────────────────────

class CanApproveLeave(HasPermission):
    required_permissions = [Permission.APPROVE_LEAVE]


class CanManageLeaveTypes(HasPermission):
    required_permissions = [Permission.MANAGE_LEAVE_TYPES]


class CanViewAllLeave(HasPermission):
    required_permissions = [Permission.VIEW_ALL_LEAVE]


# ── Attendance ────────────────────────────────────────────────────────────────

class CanEditAttendance(HasPermission):
    required_permissions = [Permission.EDIT_ATTENDANCE]


class CanExportAttendance(HasPermission):
    required_permissions = [Permission.EXPORT_ATTENDANCE]


# ── Payroll ───────────────────────────────────────────────────────────────────

class CanViewAllPayslips(HasPermission):
    required_permissions = [Permission.VIEW_ALL_PAYSLIPS]


class CanProcessPayroll(HasPermission):
    required_permissions = [Permission.PROCESS_PAYROLL]


class CanApprovePayroll(HasPermission):
    required_permissions = [Permission.APPROVE_PAYROLL]


# ── Recruitment ───────────────────────────────────────────────────────────────

class CanManageRecruitment(HasPermission):
    required_permissions = [Permission.MANAGE_JOB_POSTINGS, Permission.MANAGE_APPLICANTS]


class CanMakeOffer(HasPermission):
    required_permissions = [Permission.MAKE_OFFER]


# ── Performance ───────────────────────────────────────────────────────────────

class CanManagePerformanceCycles(HasPermission):
    required_permissions = [Permission.MANAGE_PERFORMANCE_CYCLES]


class CanViewAllPerformance(HasPermission):
    required_permissions = [Permission.VIEW_ALL_PERFORMANCE]


# ── Finance ───────────────────────────────────────────────────────────────────

class CanManageBudget(HasPermission):
    required_permissions = [Permission.MANAGE_BUDGET]


class CanApproveExpenses(HasPermission):
    required_permissions = [Permission.APPROVE_EXPENSES]


class CanViewFinancialReports(HasPermission):
    required_permissions = [Permission.VIEW_FINANCIAL_REPORTS]


class CanViewAuditTrail(HasPermission):
    required_permissions = [Permission.VIEW_AUDIT_TRAIL]


# ── IT / System ───────────────────────────────────────────────────────────────

class CanManageUsers(HasPermission):
    required_permissions = [Permission.MANAGE_USERS]


class CanManageRoles(HasPermission):
    required_permissions = [Permission.MANAGE_ROLES]


class CanAccessAuditLogs(HasPermission):
    required_permissions = [Permission.ACCESS_AUDIT_LOGS]


class CanManageSystemConfig(HasPermission):
    required_permissions = [Permission.MANAGE_SYSTEM_CONFIG]


# ── Reports ───────────────────────────────────────────────────────────────────

class CanViewCompanyReports(HasPermission):
    required_permissions = [Permission.VIEW_COMPANY_REPORTS]


class CanExportReports(HasPermission):
    required_permissions = [Permission.EXPORT_REPORTS]


# ── Announcements ─────────────────────────────────────────────────────────────

class CanManageAnnouncements(HasPermission):
    required_permissions = [Permission.MANAGE_ANNOUNCEMENTS]


# ── Operations ────────────────────────────────────────────────────────────────

class CanManageInventory(HasPermission):
    required_permissions = [Permission.MANAGE_INVENTORY]


class CanManageLogistics(HasPermission):
    required_permissions = [Permission.MANAGE_LOGISTICS]


# ── Safety & Security ─────────────────────────────────────────────────────────

class CanManageSafetyProtocols(HasPermission):
    required_permissions = [Permission.MANAGE_SAFETY_PROTOCOLS]


class CanManageSecurityAccess(HasPermission):
    required_permissions = [Permission.MANAGE_SECURITY_ACCESS]
