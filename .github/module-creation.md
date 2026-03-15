# Module Creation Guidelines

This document is the authoritative guide for creating new independent application modules that depend on the Core module set. Follow every step in order — skipping steps leads to inconsistencies that are difficult to fix later.

---

## Table of Contents

1. [Module Taxonomy](#1-module-taxonomy)
2. [Core Modules (Do Not Modify Without Review)](#2-core-modules-do-not-modify-without-review)
3. [Independent Modules to Implement](#3-independent-modules-to-implement)
4. [Directory Structure](#4-directory-structure)
5. [Step-by-Step Creation Checklist](#5-step-by-step-creation-checklist)
   - [Step 1 – Scaffold the Module](#step-1--scaffold-the-module)
   - [Step 2 – Register the App](#step-2--register-the-app)
   - [Step 3 – Define Constants](#step-3--define-constants)
   - [Step 4 – Create Models](#step-4--create-models)
   - [Step 5 – Create Managers & QuerySets](#step-5--create-managers--querysets)
   - [Step 6 – Create Selectors](#step-6--create-selectors)
   - [Step 7 – Create Services](#step-7--create-services)
   - [Step 8 – Create Forms](#step-8--create-forms)
   - [Step 9 – Create Views](#step-9--create-views)
   - [Step 10 – Wire URLs](#step-10--wire-urls)
   - [Step 11 – Register Admin](#step-11--register-admin)
   - [Step 12 – Run Migrations](#step-12--run-migrations)
   - [Step 13 – Create Factories](#step-13--create-factories)
   - [Step 14 – Write Tests](#step-14--write-tests)
6. [Patterns & Conventions Reference](#6-patterns--conventions-reference)
7. [Do's and Don'ts](#7-dos-and-donts)

---

## 1. Module Taxonomy

| Type | Location | Description |
|---|---|---|
| **Core modules** | `modules/` | Authentication primitives and user identity. Never import from `applications/` here. |
| **Application modules** | `applications/` | Domain-specific features. May import from `modules/` and from other `applications/` modules, but must avoid circular imports. |

New independent modules always go under `applications/`.

---

## 2. Core Modules (Do Not Modify Without Review)

These modules are foundational. New modules depend on them but do not alter them.

| Module | Path | Provides |
|---|---|---|
| `user` | `modules/user/` | Custom `User` model, `AUTH_USER_MODEL` |
| `auth` | `modules/auth/` | JWT login/logout, permission classes, `HasRole`, `HasPermission` |
| `employee` | `applications/employee/` | `Employee` entity, emergency contacts |
| `organization` | `applications/organization/` | `Department`, `JobTitle` |
| `employment` | `applications/employment/` | `Employment`, `Contract`, `Salary` |

### Canonical Import Paths

```python
# User model – always use settings.AUTH_USER_MODEL in model ForeignKeys
from django.conf import settings  # settings.AUTH_USER_MODEL

# Direct import for business logic / type hints
from modules.user.models import User

# Employee entity
from applications.employee.models import Employee

# Organization
from applications.organization.models import Department, JobTitle

# Employment
from applications.employment.models import Employment
```

---

## 3. Independent Modules to Implement

| Module | Path | Primary Dependency |
|---|---|---|
| **Attendance** | `applications/attendance/` | `Employee` |
| **Payroll** | `applications/payroll/` | `Employment`, `Employee` |
| **HSE** | `applications/hse/` | `Employee`, `Department` |

---

## 4. Directory Structure

Every new module must follow this exact layout:

```
applications/<module_name>/
├── __init__.py
├── apps.py           # AppConfig
├── constants.py      # StrEnum definitions for all choices
├── models.py         # ORM models extending BaseModel
├── managers.py       # Custom QuerySet and Manager classes
├── selectors.py      # Read-only query functions (no writes)
├── services.py       # Business logic / write operations
├── forms.py          # Django ModelForms for template views
├── views.py          # Class-Based Views (LoginRequiredMixin)
├── urls.py           # URL patterns with app_name namespace
├── admin.py          # ModelAdmin + Inline registrations
├── migrations/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py   # Module-local fixtures
    └── test_<domain>.py
```

> `services.py` and `forms.py` are only required when the module has write operations or form-based UI. Include them from the start if either is anticipated.

---

## 5. Step-by-Step Creation Checklist

---

### Step 1 – Scaffold the Module

Create every file in the structure above with minimal stubs. Empty `__init__.py` and placeholder comments are acceptable at this stage. This ensures the app is importable before any logic is added.

**`applications/<module_name>/apps.py`**

```python
from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = "applications.attendance"
```

> Replace `AttendanceConfig` and `"applications.attendance"` with the actual module name.

---

### Step 2 – Register the App

**2a. Add to `INTERNAL_APPS` in `config/settings/base.py`**

```python
INTERNAL_APPS = [
    "applications.organization",
    "applications.employee",
    "applications.employment",
    "applications.imports",
    "applications.company_profile",
    "applications.attendance",
    "applications.<new_module>",   # ← add here
    "shared",
]
```

**2b. Mount the URL namespace in `config/urls.py`**

```python
urlpatterns = [
    ...
    path("attendance/", include("applications.attendance.urls")),
    path("<new_module>/", include("applications.<new_module>.urls")),
]
```

Choose a clean, lowercase, hyphen-separated URL prefix that matches the domain (e.g., `attendance/`, `payroll/`, `hse/`).

---

### Step 3 – Define Constants

All choice fields must use `StrEnum` with a `.choices()` classmethod. Never use plain string tuples directly in model fields.

**`applications/<module_name>/constants.py`**

```python
from enum import StrEnum


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    ON_LEAVE = "on_leave"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.replace("_", " ").title()) for s in cls]

    @classmethod
    def present_statuses(cls) -> list[str]:
        """Statuses that count as attendance for payroll/reporting."""
        return [cls.PRESENT, cls.LATE, cls.HALF_DAY]
```

Rules:
- Values are lowercase strings (stored in the DB)
- Display labels are derived from the name (`.replace("_", " ").title()`)
- Add domain-logic classmethods (e.g., `.present_statuses()`) when needed by services or selectors

---

### Step 4 – Create Models

All models **must** inherit from `shared.base_models.BaseModel`. This provides:
- UUID primary key (`id`)
- Audit timestamps (`created_at`, `updated_at`)
- Soft-delete support (`deleted_at`, `is_active`)
- Three managers: `objects` (excludes deleted), `all_objects`, `deleted_objects`

**`applications/<module_name>/models.py`**

```python
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.employee.models import Employee
from shared.base_models import BaseModel

from .constants import AttendanceStatus
from .managers import AttendanceRecordManager


class AttendanceRecord(BaseModel):
    """Daily attendance record for an employee."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        verbose_name=_("employee"),
    )
    date = models.DateField(_("date"))
    status = models.CharField(
        _("status"),
        max_length=30,
        choices=AttendanceStatus.choices(),
        default=AttendanceStatus.PRESENT,
    )
    check_in = models.TimeField(_("check-in time"), null=True, blank=True)
    check_out = models.TimeField(_("check-out time"), null=True, blank=True)
    notes = models.TextField(_("notes"), blank=True)

    objects = AttendanceRecordManager()

    class Meta:
        verbose_name = _("Attendance Record")
        verbose_name_plural = _("Attendance Records")
        ordering = ("-date",)
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_date_attendance")
        ]

    def __str__(self) -> str:
        return f"{self.employee} – {self.date} ({self.status})"
```

Rules:
- Use `gettext_lazy` (`_()`) on every `verbose_name` / `verbose_name_plural`
- ForeignKeys to core models always use the model class directly (not a string), except for the `User` model which must use `settings.AUTH_USER_MODEL`
- Always define `Meta.ordering` so queries have a consistent default order
- Use `UniqueConstraint` (not `unique_together`) for composite uniqueness
- Never override `save()` for business logic — that belongs in `services.py`

---

### Step 5 – Create Managers & QuerySets

Define a `QuerySet` with all reusable filter/annotation methods, then expose it via a `Manager` that applies the default soft-delete filter.

**`applications/<module_name>/managers.py`**

```python
from __future__ import annotations

from django.db import models


class AttendanceRecordQuerySet(models.QuerySet):
    def for_employee(self, employee_pk) -> "AttendanceRecordQuerySet":
        return self.filter(employee_id=employee_pk)

    def for_date_range(self, start, end) -> "AttendanceRecordQuerySet":
        return self.filter(date__gte=start, date__lte=end)

    def present(self) -> "AttendanceRecordQuerySet":
        from .constants import AttendanceStatus
        return self.filter(status__in=AttendanceStatus.present_statuses())

    def with_employee(self) -> "AttendanceRecordQuerySet":
        return self.select_related("employee__user")


class AttendanceRecordManager(models.Manager.from_queryset(AttendanceRecordQuerySet)):
    def get_queryset(self) -> AttendanceRecordQuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)
```

Rules:
- Every ForeignKey traversal used in more than one place becomes a `with_<relation>()` method
- Every recurring filter condition becomes a named method
- Manager's `get_queryset()` always applies the soft-delete guard (`deleted_at__isnull=True`)
- Use `from __future__ import annotations` to allow forward reference return types

---

### Step 6 – Create Selectors

Selectors are **read-only** functions that return QuerySets or single model instances. No writes, no side effects.

**`applications/<module_name>/selectors.py`**

```python
from django.shortcuts import get_object_or_404

from .models import AttendanceRecord


def get_attendance_list(employee_pk=None, date_range=None):
    qs = AttendanceRecord.objects.with_employee().order_by("-date")
    if employee_pk:
        qs = qs.for_employee(employee_pk)
    if date_range:
        qs = qs.for_date_range(*date_range)
    return qs


def get_attendance_record(pk) -> AttendanceRecord:
    return get_object_or_404(AttendanceRecord.objects.with_employee(), pk=pk)
```

Rules:
- Always call manager/QuerySet methods, never build raw `.filter()` calls inline in views
- Selectors live in this file only — views and services import from here
- Return type annotations are optional for QuerySets but required for single-object functions

---

### Step 7 – Create Services

Services handle all write operations and enforce business rules. They are the only layer permitted to call `model.save()`, `model.delete()`, or `QuerySet.update()`.

**`applications/<module_name>/services.py`**

```python
import structlog

from .models import AttendanceRecord
from .selectors import get_attendance_record

logger = structlog.get_logger(__name__)


def create_attendance_record(*, employee, date, status, check_in=None, check_out=None, notes="") -> AttendanceRecord:
    record = AttendanceRecord(
        employee=employee,
        date=date,
        status=status,
        check_in=check_in,
        check_out=check_out,
        notes=notes,
    )
    record.full_clean()
    record.save()
    logger.info("attendance_record_created", record_id=record.pk, employee_id=employee.pk, date=str(date))
    return record


def update_attendance_record(pk, *, status=None, check_in=None, check_out=None, notes=None) -> AttendanceRecord:
    record = get_attendance_record(pk)
    if status is not None:
        record.status = status
    if check_in is not None:
        record.check_in = check_in
    if check_out is not None:
        record.check_out = check_out
    if notes is not None:
        record.notes = notes
    record.full_clean()
    record.save()
    logger.info("attendance_record_updated", record_id=record.pk)
    return record


def delete_attendance_record(pk) -> None:
    record = get_attendance_record(pk)
    record.delete()
    logger.info("attendance_record_deleted", record_id=pk)
```

Rules:
- All service function parameters after `self` / positional entity arguments must be **keyword-only** (`*` separator)
- Always call `full_clean()` before `save()` to enforce model-level validation
- Log every mutating operation with `structlog` at `INFO` level
- Never return raw QuerySets from services — return a single model instance or `None`

---

### Step 8 – Create Forms

Forms are only needed when the module has template-based UI (not API-only). Use `ModelForm` with explicit field lists.

**`applications/<module_name>/forms.py`**

```python
from django import forms

from .constants import AttendanceStatus
from .models import AttendanceRecord


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ["employee", "date", "status", "check_in", "check_out", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "check_in": forms.TimeInput(attrs={"type": "time"}),
            "check_out": forms.TimeInput(attrs={"type": "time"}),
        }
```

Rules:
- Never use `fields = "__all__"` — always list fields explicitly
- Add `type` attribute widgets for date/time inputs to render browser native pickers
- Custom validation goes in `clean_<field>()` methods, not in services

---

### Step 9 – Create Views

All views are Class-Based Views using Django's built-in generic views. They **must not** contain business logic — delegate to selectors (reads) and services (writes).

**`applications/<module_name>/views.py`**

```python
import structlog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AttendanceRecordForm
from .models import AttendanceRecord
from .selectors import get_attendance_list, get_attendance_record
from .services import create_attendance_record, delete_attendance_record, update_attendance_record


logger = structlog.get_logger(__name__)


class AttendanceListView(LoginRequiredMixin, ListView):
    template_name = "attendance/attendance_list.html"
    context_object_name = "records"
    paginate_by = 25

    def get_queryset(self):
        qs = get_attendance_list()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(employee__first_name__icontains=q) | Q(employee__last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def form_valid(self, form):
        create_attendance_record(**form.cleaned_data)
        messages.success(self.request, "Attendance record created.")
        return super().form_valid(form)


class AttendanceDetailView(LoginRequiredMixin, DetailView):
    template_name = "attendance/attendance_detail.html"
    context_object_name = "record"

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])

    def form_valid(self, form):
        update_attendance_record(self.object.pk, **form.cleaned_data)
        messages.success(self.request, "Attendance record updated.")
        return super().form_valid(form)


class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = AttendanceRecord
    template_name = "attendance/attendance_confirm_delete.html"
    success_url = reverse_lazy("attendance:attendance-list")

    def get_object(self, queryset=None):
        return get_attendance_record(self.kwargs["pk"])

    def form_valid(self, form):
        delete_attendance_record(self.object.pk)
        messages.success(self.request, "Attendance record deleted.")
        return super().form_valid(form)
```

Rules:
- Always mix in `LoginRequiredMixin` as the **first** base class
- Use `paginate_by = 25` for list views (can be increased to 50 for dense data)
- `get_object()` must always delegate to a selector — never call `Model.objects.get()` directly in views
- `success_url` must use `reverse_lazy()`, not `reverse()`

---

### Step 10 – Wire URLs

**`applications/<module_name>/urls.py`**

```python
from django.urls import path

from .views import (
    AttendanceCreateView,
    AttendanceDeleteView,
    AttendanceDetailView,
    AttendanceListView,
    AttendanceUpdateView,
)


app_name = "attendance"

urlpatterns = [
    path("", AttendanceListView.as_view(), name="attendance-list"),
    path("new/", AttendanceCreateView.as_view(), name="attendance-create"),
    path("<uuid:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"),
    path("<uuid:pk>/edit/", AttendanceUpdateView.as_view(), name="attendance-update"),
    path("<uuid:pk>/delete/", AttendanceDeleteView.as_view(), name="attendance-delete"),
]
```

Rules:
- `app_name` is **mandatory** — it is the URL namespace used in `{% url 'attendance:attendance-list' %}`
- All primary keys are `<uuid:pk>` because `BaseModel` uses UUID PKs
- Nested resources (e.g., records under an employee) follow the pattern `<uuid:pk>/<resource>/<uuid:resource_pk>/action/`

---

### Step 11 – Register Admin

**`applications/<module_name>/admin.py`**

```python
from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status", "check_in", "check_out", "is_active", "created_at")
    list_filter = ("status", "is_active", "date")
    search_fields = ("employee__first_name", "employee__last_name", "employee__employee_id")
    ordering = ("-date",)
    readonly_fields = ("created_at", "updated_at")
```

Rules:
- Register every model with `@admin.register()`
- Always include `readonly_fields = ("created_at", "updated_at")`
- For parent-child models, use `TabularInline` with `extra = 0`

---

### Step 12 – Run Migrations

```bash
uv run python manage.py makemigrations <module_name>
uv run python manage.py migrate
```

Review the generated migration file before committing. Ensure:
- One migration per logical change
- No data migrations combined with schema changes
- Foreign key `on_delete` behaviours are intentional

---

### Step 13 – Create Factories

Add factories to **`applications/factories.py`** (not a module-local file) so all test factories remain in one central place.

```python
# Inside applications/factories.py

from applications.attendance.constants import AttendanceStatus
from applications.attendance.models import AttendanceRecord


class AttendanceRecordFactory(DjangoModelFactory):
    class Meta:
        model = AttendanceRecord

    employee = factory.SubFactory(EmployeeFactory)
    date = factory.Faker("date_this_year")
    status = AttendanceStatus.PRESENT
    check_in = factory.Faker("time_object")
    check_out = factory.Faker("time_object")
    notes = ""
```

Rules:
- Use `factory.Sequence` for fields that must be unique across the test run
- Use `factory.SubFactory` for ForeignKey relations — never hardcode PKs
- Use `factory.Faker` for realistic but random data
- Use `.build()` in tests that don't need DB access; use `FactoryClass()` for those that do

---

### Step 14 – Write Tests

Create `applications/<module_name>/tests/test_<domain>.py`. Tests must cover:

| Category | What to test |
|---|---|
| **Model** | `__str__`, properties, constraints, soft-delete cycle |
| **Manager/QuerySet** | Custom filter methods return correct records |
| **Selector** | Returns expected QuerySet; raises 404 for missing records |
| **Service** | Creates/updates/deletes correctly; raises on invalid data |
| **View** | Status codes, form submission, redirect, login-required guard |

**`applications/<module_name>/tests/test_attendance.py`**

```python
import pytest

from applications.attendance.constants import AttendanceStatus
from applications.attendance.models import AttendanceRecord
from applications.factories import AttendanceRecordFactory, EmployeeFactory


pytestmark = pytest.mark.django_db


class TestAttendanceRecordModel:
    def test_str_representation(self):
        record = AttendanceRecordFactory.build(status=AttendanceStatus.PRESENT)
        assert AttendanceStatus.PRESENT in str(record)

    def test_soft_delete_excluded_from_default_manager(self):
        record = AttendanceRecordFactory()
        pk = record.pk
        record.delete()
        assert not AttendanceRecord.objects.filter(pk=pk).exists()
        assert AttendanceRecord.all_objects.filter(pk=pk).exists()

    def test_restore_reenables_record(self):
        record = AttendanceRecordFactory()
        record.delete()
        record.restore()
        assert AttendanceRecord.objects.filter(pk=record.pk).exists()


class TestAttendanceRecordQuerySet:
    def test_for_employee_filters_correctly(self):
        emp1 = EmployeeFactory()
        emp2 = EmployeeFactory()
        AttendanceRecordFactory(employee=emp1)
        AttendanceRecordFactory(employee=emp2)
        assert AttendanceRecord.objects.for_employee(emp1.pk).count() == 1
```

Rules:
- Mark the entire module with `pytestmark = pytest.mark.django_db`
- Group tests inside classes named `TestXxx` for readability
- Use `.build()` for tests that only test Python-level behaviour (no DB hit)
- Use `FactoryClass()` only when persistence is needed for the assertion
- Coverage target: **≥ 50%** per module, measured by `pytest-cov`

---

## 6. Patterns & Conventions Reference

### Request → Response Flow

```
HTTP Request
    └── View (orchestration only)
            ├── GET  → Selector → QuerySet → Template
            └── POST → Form (validate) → Service (write) → Redirect
```

### Soft-Delete Pattern

```python
record.delete()             # soft delete  → sets deleted_at, is_active=False
record.restore()            # undo          → clears deleted_at, is_active=True
record.hard_delete()        # permanent     → use only in admin/management commands

AttendanceRecord.objects           # default: excludes deleted
AttendanceRecord.all_objects       # includes deleted
AttendanceRecord.deleted_objects   # only deleted
```

### Enum Pattern

```python
class AttendanceStatus(StrEnum):
    PRESENT = "present"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.replace("_", " ").title()) for s in cls]
```

### Structlog Pattern

```python
logger = structlog.get_logger(__name__)

# In services — bind context, then log the event
logger.info("record_created", record_id=record.pk, employee_id=employee.pk)
logger.warning("duplicate_attempt", employee_id=employee.pk, date=str(date))
logger.error("unexpected_error", exc_info=True)
```

### URL Naming Convention

```
<app_name>:<resource>-<action>
# e.g.
attendance:attendance-list
attendance:attendance-create
attendance:attendance-detail
attendance:attendance-update
attendance:attendance-delete
```

---

## 7. Do's and Don'ts

### Do's ✓

- **Do** always inherit models from `BaseModel`
- **Do** always use `StrEnum` + `.choices()` for model choice fields
- **Do** put all read queries in `selectors.py`
- **Do** put all write logic in `services.py`
- **Do** call `full_clean()` before every `save()` in services
- **Do** use `LoginRequiredMixin` as the first mixin in every view
- **Do** use `uuid:pk` in URL patterns (BaseModel uses UUID PKs)
- **Do** add `app_name` to every `urls.py`
- **Do** log every create/update/delete in services using `structlog`
- **Do** use `factory.SubFactory` for FK relations in factories
- **Do** use timezone-aware datetimes (`django.utils.timezone.now()`, not `datetime.now()`)

### Don'ts ✗

- **Don't** call `os.getenv()` — use the settings layer (`config/settings/`)
- **Don't** put `print()` in any module file — use `structlog`
- **Don't** write ORM queries directly in views — use selectors
- **Don't** put business logic in models or serializers — use services
- **Don't** use bare `except Exception` — catch specific exceptions
- **Don't** call `datetime.now()` without timezone — use `timezone.now()`
- **Don't** import from `modules/` inside another `modules/` app (core isolation)
- **Don't** create circular imports — if two modules need to share data, use a selector or a shared abstraction in `shared/`
- **Don't** hardcode URLs — use `{% url %}` in templates and `reverse_lazy()` in views
- **Don't** use `unique_together` in `Meta` — use `UniqueConstraint` instead


## 8. Additional Notes

### Attendance App
- Use jibble.com as role model in designing Attendance App (Workflow & HTML Layout)
