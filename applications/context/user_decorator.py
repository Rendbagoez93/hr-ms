from functools import wraps
from typing import ClassVar

from django.http import JsonResponse

from config.roles import Role


class RoleCheck:
    _GROUPS: ClassVar[dict] = {
        'executive':      Role.executive_roles,
        'management':     Role.management_roles,
        'hr':             Role.hr_roles,
        'finance':        Role.finance_roles,
        'it':             Role.it_roles,
        'operations':     Role.operations_roles,
        'safety_security': Role.safety_and_security_roles,
        'regular':        Role.regular_roles,
        'privileged':     Role.privileged_roles,
        'approver':       Role.approver_roles,
    }

    def __init__(self, *roles: Role):
        self.allowed_roles = frozenset(str(r) for r in roles)

    def __call__(self, view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required.'}, status=401)
            if request.user.role not in self.allowed_roles:
                return JsonResponse({'detail': 'Permission denied.'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper

    @classmethod
    def group(cls, group_name: str) -> RoleCheck:
        """Create a RoleCheck from a predefined role group name."""
        if group_name not in cls._GROUPS:
            raise ValueError(
                f"Unknown role group '{group_name}'. "
                f"Available groups: {list(cls._GROUPS)}"
            )
        return cls(*cls._GROUPS[group_name]())
