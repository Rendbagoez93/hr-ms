from enum import StrEnum


class Role(StrEnum):
    # ── Executive ─────────────────────────────────────────────────────────────
    CEO = "ceo"
    CFO = "cfo"
    COO = "coo"
    CTO = "cto"
    DIRECTOR = "director"
    VICE_PRESIDENT = "vice_president"

    # ── Management ────────────────────────────────────────────────────────────
    GENERAL_MANAGER = "general_manager"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    TEAM_LEAD = "team_lead"

    # ── Human Resources ───────────────────────────────────────────────────────
    HR_MANAGER = "hr_manager"
    HR_OFFICER = "hr_officer"
    RECRUITER = "recruiter"
    PAYROLL_OFFICER = "payroll_officer"

    # ── Finance & Accounting ──────────────────────────────────────────────────
    FINANCE_MANAGER = "finance_manager"
    ACCOUNTANT = "accountant"
    FINANCE_ANALYST = "finance_analyst"
    AUDITOR = "auditor"

    # ── IT & Technology ───────────────────────────────────────────────────────
    ADMINISTRATOR = "administrator"
    IT_MANAGER = "it_manager"
    DEVELOPER = "developer"
    SYSTEM_ANALYST = "system_analyst"
    IT_SUPPORT = "it_support"

    # ── Administrative / Clerical ─────────────────────────────────────────────
    OFFICE_MANAGER = "office_manager"
    EXECUTIVE_ASSISTANT = "executive_assistant"
    RECEPTIONIST = "receptionist"
    CLERK = "clerk"

    # ── Sales & Marketing ─────────────────────────────────────────────────────
    SALES_MANAGER = "sales_manager"
    SALES_REPRESENTATIVE = "sales_representative"
    MARKETING_SPECIALIST = "marketing_specialist"

    # ── Operations ────────────────────────────────────────────────────────────
    OPERATIONS_MANAGER = "operations_manager"
    LOGISTICS_COORDINATOR = "logistics_coordinator"
    INVENTORY_CONTROLLER = "inventory_controller"
    
    # ── Safety & Security ─────────────────────────────────────────────
    SAFETY_OFFICER = "safety_officer"
    SECURITY_OFFICER = "security_officer"

    # ── Regular / General Staff ───────────────────────────────────────────────
    STAFF = "staff"
    INTERN = "intern"
    CONTRACTOR = "contractor"
    PART_TIME = "part_time"

    # ─────────────────────────────────────────────────────────────────────────
    # Role group classmethods
    # Each group reflects a shared capability boundary within the system.
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def executive_roles(cls):
        """Full strategic access: can view all data, approve anything, and
        configure company-wide settings."""
        included = [cls.CEO, cls.CFO, cls.COO, cls.CTO, cls.DIRECTOR, cls.VICE_PRESIDENT]
        return [role.value for role in cls if role in included]

    @classmethod
    def management_roles(cls):
        """Can manage direct reports, approve leave/overtime, and access
        team-level reports."""
        included = [
            cls.GENERAL_MANAGER, cls.MANAGER, cls.SUPERVISOR, cls.TEAM_LEAD,
            cls.OPERATIONS_MANAGER, cls.SALES_MANAGER,
        ]
        return [role.value for role in cls if role in included]

    @classmethod
    def hr_roles(cls):
        """Access to employee records, recruitment pipelines, payroll processing,
        and HR reporting."""
        included = [cls.HR_MANAGER, cls.HR_OFFICER, cls.RECRUITER, cls.PAYROLL_OFFICER]
        return [role.value for role in cls if role in included]

    @classmethod
    def finance_roles(cls):
        """Access to financial statements, payroll data, budgets, and audit
        trails."""
        included = [cls.CFO, cls.FINANCE_MANAGER, cls.ACCOUNTANT, cls.FINANCE_ANALYST, cls.AUDITOR]
        return [role.value for role in cls if role in included]

    @classmethod
    def it_roles(cls):
        """System administration, user provisioning, technical configuration,
        and infrastructure access."""
        included = [cls.ADMINISTRATOR, cls.IT_MANAGER, cls.DEVELOPER, cls.SYSTEM_ANALYST, cls.IT_SUPPORT]
        return [role.value for role in cls if role in included]

    @classmethod
    def administrative_roles(cls):
        """Office operations, scheduling, document management, and front-desk
        capabilities."""
        included = [cls.OFFICE_MANAGER, cls.EXECUTIVE_ASSISTANT, cls.RECEPTIONIST, cls.CLERK]
        return [role.value for role in cls if role in included]

    @classmethod
    def sales_and_marketing_roles(cls):
        """Access to CRM data, campaign tools, sales pipelines, and
        customer-facing reports."""
        included = [cls.SALES_MANAGER, cls.SALES_REPRESENTATIVE, cls.MARKETING_SPECIALIST]
        return [role.value for role in cls if role in included]

    @classmethod
    def operations_roles(cls):
        """Access to supply chain, inventory, and logistics modules."""
        included = [cls.OPERATIONS_MANAGER, cls.LOGISTICS_COORDINATOR, cls.INVENTORY_CONTROLLER]
        return [role.value for role in cls if role in included]
    
    @classmethod
    def safety_and_security_roles(cls):
        """Access to safety protocols, incident reporting, and security
        monitoring tools."""
        included = [cls.SAFETY_OFFICER, cls.SECURITY_OFFICER]
        return [role.value for role in cls if role in included]

    @classmethod
    def regular_roles(cls):
        """Standard employee access: personal profile, payslips, leave
        requests, and company announcements only."""
        included = [cls.STAFF, cls.INTERN, cls.CONTRACTOR, cls.PART_TIME]
        return [role.value for role in cls if role in included]

    @classmethod
    def privileged_roles(cls):
        """Union of executive + IT roles that can bypass standard permission
        checks (e.g. impersonation, audit log access)."""
        return list(dict.fromkeys(cls.executive_roles() + cls.it_roles()))

    @classmethod
    def approver_roles(cls):
        """Roles that are allowed to approve employee requests such as leave,
        expense claims, and overtime."""
        return list(dict.fromkeys(cls.executive_roles() + cls.management_roles() + cls.hr_roles()))

    @classmethod
    def all_roles(cls):
        """Return every defined role value."""
        return [role.value for role in cls]
