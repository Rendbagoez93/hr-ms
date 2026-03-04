from enum import StrEnum

from config.roles import Role


# ─────────────────────────────────────────────────────────────────────────────
# Permission catalogue
# Every capability recognised by the system is declared here as a StrEnum so
# that permissions can be used as plain strings in HTTP responses, stored in
# tokens, and compared without importing the enum everywhere.
# ─────────────────────────────────────────────────────────────────────────────

class Permission(StrEnum):
    # ── Employee / Profile ────────────────────────────────────────────────────
    VIEW_OWN_PROFILE            = "view_own_profile"
    EDIT_OWN_PROFILE            = "edit_own_profile"
    VIEW_EMPLOYEE_LIST          = "view_employee_list"
    VIEW_EMPLOYEE_DETAIL        = "view_employee_detail"
    CREATE_EMPLOYEE             = "create_employee"
    EDIT_EMPLOYEE               = "edit_employee"
    DELETE_EMPLOYEE             = "delete_employee"
    EXPORT_EMPLOYEE_DATA        = "export_employee_data"

    # ── Leave ─────────────────────────────────────────────────────────────────
    SUBMIT_LEAVE_REQUEST        = "submit_leave_request"
    VIEW_OWN_LEAVE              = "view_own_leave"
    VIEW_TEAM_LEAVE             = "view_team_leave"
    VIEW_ALL_LEAVE              = "view_all_leave"
    APPROVE_LEAVE               = "approve_leave"
    REJECT_LEAVE                = "reject_leave"
    MANAGE_LEAVE_TYPES          = "manage_leave_types"

    # ── Attendance ────────────────────────────────────────────────────────────
    VIEW_OWN_ATTENDANCE         = "view_own_attendance"
    VIEW_TEAM_ATTENDANCE        = "view_team_attendance"
    VIEW_ALL_ATTENDANCE         = "view_all_attendance"
    EDIT_ATTENDANCE             = "edit_attendance"
    EXPORT_ATTENDANCE           = "export_attendance"

    # ── Payroll ───────────────────────────────────────────────────────────────
    VIEW_OWN_PAYSLIP            = "view_own_payslip"
    VIEW_ALL_PAYSLIPS           = "view_all_payslips"
    PROCESS_PAYROLL             = "process_payroll"
    APPROVE_PAYROLL             = "approve_payroll"
    EXPORT_PAYROLL              = "export_payroll"

    # ── Recruitment ───────────────────────────────────────────────────────────
    VIEW_JOB_POSTINGS           = "view_job_postings"
    CREATE_JOB_POSTING          = "create_job_posting"
    MANAGE_JOB_POSTINGS         = "manage_job_postings"
    VIEW_APPLICANTS             = "view_applicants"
    MANAGE_APPLICANTS           = "manage_applicants"
    SCHEDULE_INTERVIEW          = "schedule_interview"
    MAKE_OFFER                  = "make_offer"

    # ── Performance ───────────────────────────────────────────────────────────
    SUBMIT_SELF_REVIEW          = "submit_self_review"
    VIEW_OWN_PERFORMANCE        = "view_own_performance"
    REVIEW_TEAM_PERFORMANCE     = "review_team_performance"
    VIEW_ALL_PERFORMANCE        = "view_all_performance"
    MANAGE_PERFORMANCE_CYCLES   = "manage_performance_cycles"

    # ── Finance / Budget ──────────────────────────────────────────────────────
    VIEW_BUDGET                 = "view_budget"
    MANAGE_BUDGET               = "manage_budget"
    VIEW_FINANCIAL_REPORTS      = "view_financial_reports"
    APPROVE_EXPENSES            = "approve_expenses"
    MANAGE_EXPENSES             = "manage_expenses"
    VIEW_AUDIT_TRAIL            = "view_audit_trail"

    # ── IT / System ───────────────────────────────────────────────────────────
    MANAGE_USERS                = "manage_users"
    MANAGE_ROLES                = "manage_roles"
    VIEW_SYSTEM_LOGS            = "view_system_logs"
    MANAGE_SYSTEM_CONFIG        = "manage_system_config"
    MANAGE_INTEGRATIONS         = "manage_integrations"
    ACCESS_AUDIT_LOGS           = "access_audit_logs"

    # ── Reports ───────────────────────────────────────────────────────────────
    VIEW_OWN_REPORTS            = "view_own_reports"
    VIEW_TEAM_REPORTS           = "view_team_reports"
    VIEW_DEPARTMENT_REPORTS     = "view_department_reports"
    VIEW_COMPANY_REPORTS        = "view_company_reports"
    EXPORT_REPORTS              = "export_reports"

    # ── Announcements ─────────────────────────────────────────────────────────
    VIEW_ANNOUNCEMENTS          = "view_announcements"
    CREATE_ANNOUNCEMENTS        = "create_announcements"
    MANAGE_ANNOUNCEMENTS        = "manage_announcements"

    # ── Operations / Logistics / Inventory ────────────────────────────────────
    VIEW_INVENTORY              = "view_inventory"
    MANAGE_INVENTORY            = "manage_inventory"
    VIEW_LOGISTICS              = "view_logistics"
    MANAGE_LOGISTICS            = "manage_logistics"
    VIEW_OPERATIONS_REPORTS     = "view_operations_reports"

    # ── Safety & Security ─────────────────────────────────────────────────────
    VIEW_SAFETY_PROTOCOLS       = "view_safety_protocols"
    MANAGE_SAFETY_PROTOCOLS     = "manage_safety_protocols"
    SUBMIT_INCIDENT_REPORT      = "submit_incident_report"
    VIEW_INCIDENT_REPORTS       = "view_incident_reports"
    MANAGE_SECURITY_ACCESS      = "manage_security_access"

    # ── Administrative / Office ───────────────────────────────────────────────
    MANAGE_OFFICE_RESOURCES     = "manage_office_resources"
    SCHEDULE_MEETINGS           = "schedule_meetings"
    MANAGE_DOCUMENTS            = "manage_documents"
    HANDLE_RECEPTION            = "handle_reception"


# ─────────────────────────────────────────────────────────────────────────────
# Shared permission groups
#
# Permissions are composed bottom-up:  _BASE is included in every group so
# that per-role sets stay DRY.  Roles at the same organisational level share
# the same group constant and can be extended individually when needed.
# ─────────────────────────────────────────────────────────────────────────────

# Every authenticated employee – regardless of role
_BASE: frozenset[Permission] = frozenset({
    Permission.VIEW_OWN_PROFILE,
    Permission.EDIT_OWN_PROFILE,
    Permission.SUBMIT_LEAVE_REQUEST,
    Permission.VIEW_OWN_LEAVE,
    Permission.VIEW_OWN_ATTENDANCE,
    Permission.VIEW_OWN_PAYSLIP,
    Permission.SUBMIT_SELF_REVIEW,
    Permission.VIEW_OWN_PERFORMANCE,
    Permission.VIEW_OWN_REPORTS,
    Permission.VIEW_ANNOUNCEMENTS,
    Permission.SUBMIT_INCIDENT_REPORT,  # everyone may report a safety incident
})

# ── Management level (GENERAL_MANAGER, MANAGER, SUPERVISOR, TEAM_LEAD) ───────
# Responsibilities: oversee direct reports, approve requests, run team reports
_MANAGEMENT_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.VIEW_EMPLOYEE_DETAIL,
    Permission.VIEW_TEAM_LEAVE,
    Permission.APPROVE_LEAVE,
    Permission.REJECT_LEAVE,
    Permission.VIEW_TEAM_ATTENDANCE,
    Permission.REVIEW_TEAM_PERFORMANCE,
    Permission.VIEW_TEAM_REPORTS,
    Permission.APPROVE_EXPENSES,
    Permission.CREATE_ANNOUNCEMENTS,
    Permission.SCHEDULE_MEETINGS,
    Permission.MANAGE_DOCUMENTS,
})

# ── Human Resources group ─────────────────────────────────────────────────────
# Responsibilities: employee lifecycle, payroll, recruitment, compliance
_HR_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.VIEW_EMPLOYEE_DETAIL,
    Permission.CREATE_EMPLOYEE,
    Permission.EDIT_EMPLOYEE,
    Permission.EXPORT_EMPLOYEE_DATA,
    Permission.VIEW_ALL_LEAVE,
    Permission.APPROVE_LEAVE,
    Permission.REJECT_LEAVE,
    Permission.MANAGE_LEAVE_TYPES,
    Permission.VIEW_ALL_ATTENDANCE,
    Permission.EDIT_ATTENDANCE,
    Permission.EXPORT_ATTENDANCE,
    Permission.VIEW_ALL_PAYSLIPS,
    Permission.PROCESS_PAYROLL,
    Permission.EXPORT_PAYROLL,
    Permission.VIEW_JOB_POSTINGS,
    Permission.CREATE_JOB_POSTING,
    Permission.MANAGE_JOB_POSTINGS,
    Permission.VIEW_APPLICANTS,
    Permission.MANAGE_APPLICANTS,
    Permission.SCHEDULE_INTERVIEW,
    Permission.MAKE_OFFER,
    Permission.VIEW_ALL_PERFORMANCE,
    Permission.MANAGE_PERFORMANCE_CYCLES,
    Permission.VIEW_DEPARTMENT_REPORTS,
    Permission.EXPORT_REPORTS,
    Permission.MANAGE_DOCUMENTS,
    Permission.SCHEDULE_MEETINGS,
})

# ── Finance group ─────────────────────────────────────────────────────────────
# Responsibilities: financial reporting, expense oversight, budget visibility
_FINANCE_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_BUDGET,
    Permission.VIEW_FINANCIAL_REPORTS,
    Permission.VIEW_ALL_PAYSLIPS,
    Permission.APPROVE_EXPENSES,
    Permission.MANAGE_EXPENSES,
    Permission.VIEW_AUDIT_TRAIL,
    Permission.VIEW_COMPANY_REPORTS,
    Permission.EXPORT_REPORTS,
    Permission.EXPORT_PAYROLL,
    Permission.VIEW_DEPARTMENT_REPORTS,
})

# Finance managers / CFO can additionally manage the budget and approve payroll
_FINANCE_SENIOR_PERMS: frozenset[Permission] = _FINANCE_PERMS | frozenset({
    Permission.MANAGE_BUDGET,
    Permission.APPROVE_PAYROLL,
})

# ── IT / Technology group ─────────────────────────────────────────────────────
# Responsibilities: user provisioning, system config, integrations, audit access
_IT_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.MANAGE_USERS,
    Permission.MANAGE_ROLES,
    Permission.VIEW_SYSTEM_LOGS,
    Permission.MANAGE_SYSTEM_CONFIG,
    Permission.MANAGE_INTEGRATIONS,
    Permission.ACCESS_AUDIT_LOGS,
    Permission.VIEW_DEPARTMENT_REPORTS,
    Permission.MANAGE_DOCUMENTS,
})

# ── Administrative / Office group ─────────────────────────────────────────────
# Responsibilities: office logistics, scheduling, document control, reception
_ADMIN_OFFICE_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.MANAGE_OFFICE_RESOURCES,
    Permission.SCHEDULE_MEETINGS,
    Permission.MANAGE_DOCUMENTS,
    Permission.HANDLE_RECEPTION,
    Permission.CREATE_ANNOUNCEMENTS,
    Permission.VIEW_TEAM_REPORTS,
})

# ── Sales & Marketing group ───────────────────────────────────────────────────
# Responsibilities: pipelines, campaigns, customer-facing communications
_SALES_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_JOB_POSTINGS,
    Permission.VIEW_OPERATIONS_REPORTS,
    Permission.CREATE_ANNOUNCEMENTS,
    Permission.MANAGE_DOCUMENTS,
    Permission.SCHEDULE_MEETINGS,
    Permission.VIEW_TEAM_REPORTS,
})

# ── Operations group ──────────────────────────────────────────────────────────
# Responsibilities: inventory, supply chain, logistics coordination
_OPERATIONS_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.VIEW_INVENTORY,
    Permission.MANAGE_INVENTORY,
    Permission.VIEW_LOGISTICS,
    Permission.MANAGE_LOGISTICS,
    Permission.VIEW_OPERATIONS_REPORTS,
    Permission.VIEW_TEAM_REPORTS,
    Permission.MANAGE_DOCUMENTS,
})

# ── Safety & Security group ───────────────────────────────────────────────────
# Responsibilities: incident management, safety compliance, access control
_SAFETY_PERMS: frozenset[Permission] = _BASE | frozenset({
    Permission.VIEW_EMPLOYEE_LIST,
    Permission.VIEW_SAFETY_PROTOCOLS,
    Permission.MANAGE_SAFETY_PROTOCOLS,
    Permission.VIEW_INCIDENT_REPORTS,
    Permission.MANAGE_SECURITY_ACCESS,
    Permission.VIEW_DEPARTMENT_REPORTS,
    Permission.MANAGE_DOCUMENTS,
})

# ── Executive – full access ───────────────────────────────────────────────────
# Responsibilities: company-wide strategy, final approvals, all data visibility
_EXECUTIVE_PERMS: frozenset[Permission] = frozenset(Permission)


# ─────────────────────────────────────────────────────────────────────────────
# ROLE_PERMISSIONS
#
# Maps every Role to the frozenset of Permission values it holds.
# Same-level roles that share a group constant are listed together.
# Individual roles may layer additional capabilities on top of their group.
# ─────────────────────────────────────────────────────────────────────────────

ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {

    # ── Executive ─────────────────────────────────────────────────────────────
    # Same level: CEO / COO / CTO / DIRECTOR / VICE_PRESIDENT
    # Full system access; CFO gets an extra explicit finance layer (no-op since
    # _EXECUTIVE_PERMS already covers everything, but signals intent clearly).
    Role.CEO:             _EXECUTIVE_PERMS,
    Role.COO:             _EXECUTIVE_PERMS,
    Role.CTO:             _EXECUTIVE_PERMS,
    Role.DIRECTOR:        _EXECUTIVE_PERMS,
    Role.VICE_PRESIDENT:  _EXECUTIVE_PERMS,
    Role.CFO:             _EXECUTIVE_PERMS | _FINANCE_SENIOR_PERMS,  # explicit finance intent

    # ── Management ────────────────────────────────────────────────────────────
    # Same level: GENERAL_MANAGER / MANAGER / SUPERVISOR / TEAM_LEAD
    # GENERAL_MANAGER gets broader visibility (all leave, all attendance, dept reports).
    Role.GENERAL_MANAGER: _MANAGEMENT_PERMS | frozenset({
        Permission.VIEW_ALL_LEAVE,
        Permission.VIEW_ALL_ATTENDANCE,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.MANAGE_ANNOUNCEMENTS,
        Permission.DELETE_EMPLOYEE,         # can offboard within department
    }),
    Role.MANAGER:         _MANAGEMENT_PERMS,
    Role.SUPERVISOR:      _MANAGEMENT_PERMS,
    Role.TEAM_LEAD:       _MANAGEMENT_PERMS,

    # ── Human Resources ───────────────────────────────────────────────────────
    # HR_MANAGER: full HR remit + delete employee + payroll approval
    Role.HR_MANAGER: _HR_PERMS | frozenset({
        Permission.DELETE_EMPLOYEE,
        Permission.APPROVE_PAYROLL,
        Permission.MANAGE_ANNOUNCEMENTS,
        Permission.VIEW_COMPANY_REPORTS,
    }),
    # HR_OFFICER: day-to-day HR operations; cannot delete or approve payroll
    Role.HR_OFFICER: _HR_PERMS,
    # RECRUITER: focused on talent acquisition; no payroll or performance cycles
    Role.RECRUITER: _BASE | frozenset({
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.VIEW_JOB_POSTINGS,
        Permission.CREATE_JOB_POSTING,
        Permission.MANAGE_JOB_POSTINGS,
        Permission.VIEW_APPLICANTS,
        Permission.MANAGE_APPLICANTS,
        Permission.SCHEDULE_INTERVIEW,
        Permission.MAKE_OFFER,
        Permission.MANAGE_DOCUMENTS,
        Permission.SCHEDULE_MEETINGS,
        Permission.VIEW_DEPARTMENT_REPORTS,
    }),
    # PAYROLL_OFFICER: focused on compensation; no recruitment or performance
    Role.PAYROLL_OFFICER: _BASE | frozenset({
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.VIEW_EMPLOYEE_DETAIL,
        Permission.VIEW_ALL_PAYSLIPS,
        Permission.PROCESS_PAYROLL,
        Permission.EXPORT_PAYROLL,
        Permission.VIEW_ALL_ATTENDANCE,
        Permission.EXPORT_ATTENDANCE,
        Permission.MANAGE_EXPENSES,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.EXPORT_REPORTS,
    }),

    # ── Finance & Accounting ──────────────────────────────────────────────────
    # FINANCE_MANAGER: full finance remit including budget management
    Role.FINANCE_MANAGER:  _FINANCE_SENIOR_PERMS,
    # ACCOUNTANT: day-to-day financial operations; no budget management
    Role.ACCOUNTANT:       _FINANCE_PERMS,
    # FINANCE_ANALYST: read-heavy; no expense approval or payroll export
    Role.FINANCE_ANALYST:  _BASE | frozenset({
        Permission.VIEW_BUDGET,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.VIEW_ALL_PAYSLIPS,
        Permission.VIEW_AUDIT_TRAIL,
        Permission.VIEW_COMPANY_REPORTS,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.EXPORT_REPORTS,
    }),
    # AUDITOR: read + audit trail access; cannot modify financial data
    Role.AUDITOR:          _BASE | frozenset({
        Permission.VIEW_BUDGET,
        Permission.VIEW_FINANCIAL_REPORTS,
        Permission.VIEW_ALL_PAYSLIPS,
        Permission.VIEW_AUDIT_TRAIL,
        Permission.ACCESS_AUDIT_LOGS,
        Permission.VIEW_SYSTEM_LOGS,
        Permission.VIEW_COMPANY_REPORTS,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.EXPORT_REPORTS,
        Permission.EXPORT_PAYROLL,
        Permission.VIEW_EMPLOYEE_LIST,
    }),

    # ── IT & Technology ───────────────────────────────────────────────────────
    # ADMINISTRATOR / IT_MANAGER: full IT authority
    Role.ADMINISTRATOR: _IT_PERMS,
    Role.IT_MANAGER:    _IT_PERMS | frozenset({
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.MANAGE_ANNOUNCEMENTS,
    }),
    # DEVELOPER: access to system internals; no user/role provisioning
    Role.DEVELOPER: _BASE | frozenset({
        Permission.VIEW_SYSTEM_LOGS,
        Permission.MANAGE_INTEGRATIONS,
        Permission.ACCESS_AUDIT_LOGS,
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.MANAGE_DOCUMENTS,
    }),
    # SYSTEM_ANALYST: read + audit; no provisioning or config changes
    Role.SYSTEM_ANALYST: _BASE | frozenset({
        Permission.VIEW_SYSTEM_LOGS,
        Permission.ACCESS_AUDIT_LOGS,
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.VIEW_OPERATIONS_REPORTS,
        Permission.MANAGE_DOCUMENTS,
    }),
    # IT_SUPPORT: user-facing support; limited system access
    Role.IT_SUPPORT: _BASE | frozenset({
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.VIEW_EMPLOYEE_DETAIL,
        Permission.VIEW_SYSTEM_LOGS,
        Permission.MANAGE_DOCUMENTS,
        Permission.SCHEDULE_MEETINGS,
    }),

    # ── Administrative / Clerical ─────────────────────────────────────────────
    # Same level: OFFICE_MANAGER / EXECUTIVE_ASSISTANT / RECEPTIONIST / CLERK
    # OFFICE_MANAGER: full admin remit + team reports + announcements
    Role.OFFICE_MANAGER: _ADMIN_OFFICE_PERMS | frozenset({
        Permission.MANAGE_ANNOUNCEMENTS,
        Permission.VIEW_TEAM_REPORTS,
    }),
    # EXECUTIVE_ASSISTANT: supports executives; broader visibility
    Role.EXECUTIVE_ASSISTANT: _ADMIN_OFFICE_PERMS | frozenset({
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.VIEW_EMPLOYEE_DETAIL,
    }),
    # RECEPTIONIST: front-desk duties only
    Role.RECEPTIONIST: _BASE | frozenset({
        Permission.VIEW_EMPLOYEE_LIST,
        Permission.HANDLE_RECEPTION,
        Permission.SCHEDULE_MEETINGS,
        Permission.MANAGE_DOCUMENTS,
    }),
    # CLERK: document and data entry
    Role.CLERK: _BASE | frozenset({
        Permission.MANAGE_DOCUMENTS,
        Permission.HANDLE_RECEPTION,
        Permission.VIEW_EMPLOYEE_LIST,
    }),

    # ── Sales & Marketing ─────────────────────────────────────────────────────
    # SALES_MANAGER: management perms + sales domain
    Role.SALES_MANAGER: _MANAGEMENT_PERMS | _SALES_PERMS | frozenset({
        Permission.VIEW_DEPARTMENT_REPORTS,
        Permission.MANAGE_ANNOUNCEMENTS,
    }),
    # SALES_REPRESENTATIVE / MARKETING_SPECIALIST: same base sales perms
    Role.SALES_REPRESENTATIVE:  _SALES_PERMS,
    Role.MARKETING_SPECIALIST:  _SALES_PERMS | frozenset({
        Permission.MANAGE_ANNOUNCEMENTS,  # publishes campaigns / comms
    }),

    # ── Operations ────────────────────────────────────────────────────────────
    # OPERATIONS_MANAGER: management + full operations domain
    Role.OPERATIONS_MANAGER: _MANAGEMENT_PERMS | _OPERATIONS_PERMS | frozenset({
        Permission.VIEW_DEPARTMENT_REPORTS,
    }),
    # LOGISTICS_COORDINATOR: logistics focus; no inventory management
    Role.LOGISTICS_COORDINATOR: _BASE | frozenset({
        Permission.VIEW_INVENTORY,
        Permission.VIEW_LOGISTICS,
        Permission.MANAGE_LOGISTICS,
        Permission.VIEW_OPERATIONS_REPORTS,
        Permission.VIEW_TEAM_REPORTS,
        Permission.MANAGE_DOCUMENTS,
    }),
    # INVENTORY_CONTROLLER: inventory focus; no logistics management
    Role.INVENTORY_CONTROLLER: _BASE | frozenset({
        Permission.VIEW_INVENTORY,
        Permission.MANAGE_INVENTORY,
        Permission.VIEW_LOGISTICS,
        Permission.VIEW_OPERATIONS_REPORTS,
        Permission.VIEW_TEAM_REPORTS,
        Permission.MANAGE_DOCUMENTS,
    }),

    # ── Safety & Security ─────────────────────────────────────────────────────
    # Same level: SAFETY_OFFICER / SECURITY_OFFICER
    Role.SAFETY_OFFICER:   _SAFETY_PERMS,
    Role.SECURITY_OFFICER: _SAFETY_PERMS,

    # ── Regular / General Staff ───────────────────────────────────────────────
    # Same level: STAFF / INTERN / CONTRACTOR / PART_TIME
    # Standard employee self-service access only.
    Role.STAFF:       _BASE,
    Role.INTERN:      _BASE,
    Role.CONTRACTOR:  _BASE,
    Role.PART_TIME:   _BASE,
}
