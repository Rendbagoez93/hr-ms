# Project Overview (HR MS - Human Resource Management System)

- **Framework**: Django 6.0 (ASGI)
- **Python**: 3.14+
- **Config**: `pydantic-settings` from `.env`, `structlog` via YAML
- **Database**: SQLite (for development), PostgreSQL (for production)
- **API**: Django REST Framework (DRF)
- **Testing**: `pytest` + `pytest-django` + `factory_boy` + `pytest-cov`
- **Common Apps location**: `modules/` directory
- **Shared utilities**: `shared/` directory (e.g., base models, monads)
- **Main Application**: `applications/` for installed applications, context processors, and guard decorators
- **Settings**: `config/settings/` (split by environment)
- **Dependency manager**: `uv` + `pyproject.toml`

---

## Folder Structure

```
hr-ms/
├── .github/
│   └── copilot-instructions.md     # Copilot workspace instructions
├── applications/
│   └── context/
│       └── user_decorator.py       # Custom template context processors
├── assets/                         # Static assets (images, icons, etc.)
├── config/
│   ├── asgi.py                     # ASGI entry point
│   ├── wsgi.py                     # WSGI entry point
│   ├── roles.py                    # Global role definitions
│   ├── urls.py                     # Root URL configuration
│   └── settings/
│       ├── base.py                 # Base settings shared across all environments
│       ├── envcommon.py            # Environment variable loading (pydantic-settings)
│       ├── databases.py            # Database configuration
│       ├── companyconf.py          # Company-level configuration (from YAML)
│       ├── factory.py              # Test/factory-related settings
│       └── local.py                # Local development settings
├── modules/                        # Django app modules (one sub-folder per domain)
│   ├── auth/                       # Authentication & authorization app
│   │   ├── apps.py
│   │   ├── constant.py             # Auth-specific constants
│   │   ├── permissions.py          # DRF permission classes
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │       ├── conftest.py
│   │       ├── test_permissions.py
│   │       ├── test_serializers.py
│   │       └── test_views.py
│   └── user/                       # User management app
│       ├── admin.py
│       ├── apps.py
│       ├── managers.py             # Custom QuerySet / Manager classes
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       │   └── 0001_initial.py
│       └── tests/
│           ├── conftest.py
│           ├── test_email_normalization.py
│           ├── test_role_transition.py
│           └── test_soft_delete.py
├── shared/                         # Shared utilities used across modules
│   ├── base_models.py              # Abstract base models (e.g., TimeStampedModel)
│   └── monad.py                    # Functional monad helpers
├── templates/                      # Django HTML templates
├── tests/                          # Top-level integration / config tests
│   ├── conftest.py
│   ├── settings/                   # Tests for config/settings modules
│   │   ├── test_companyconf.py
│   │   ├── test_databases.py
│   │   ├── test_envcommon.py
│   │   └── test_factory.py
│   └── shared/                     # Tests for shared utilities
│       ├── test_base_models.py
│       └── test_monad.py
├── company_config.yaml             # Company-level runtime configuration
├── company_config_schema.json      # JSON Schema for company_config.yaml validation
├── manage.py                       # Django management CLI
├── pyproject.toml                  # Project metadata, dependencies, ruff/pytest config
└── uv.lock                         # Locked dependency versions (uv)
```

---

## Product Vision

### What Is HR-MS?

The Human Resource Management System (HR-MS) is a comprehensive web application that serves as a central repository for all employee information. This system will streamline HR processes, improve data accuracy, and provide a solid foundation for future module integrations.

### Core Domain Concepts

| Concept | Description |
|---|---|
| **Employee** | The central entity representing an employee. Contains all personal and professional data. |
| **Personal Information** | Details like name, address, contact information, date of birth, etc. |
| **Employment Details** | Job title, department, reporting manager, work location, and employment status (e.g., full-time, part-time, contract). |
| **Contract** | Details of the employment contract, including start date, end date (if applicable), contract type, and terms. |
| **Salary** | Information about the employee's salary, including pay grade, amount, and payment frequency. |
| **Emergency Contact** | Information for one or more emergency contacts for the employee. |
| **Department** | An organizational unit within the company (e.g., Engineering, Sales, HR). |
| **Job Title** | The specific role or position held by an employee (e.g., Software Engineer, Sales Manager). |

### Future Goals / Roadmap

- **Attendance Module**: Track employee attendance, leaves, and work hours.
- **Payroll Module**: Automate payroll calculation and processing.
- **HSE Module**: Manage Health, Safety, and Environment related incidents and training.
- **Man-Hours Module**: Track man-hours for specific projects or tasks.
- **Self-Service Portal**: Allow employees to view and manage their own information, request leave, and access company documents.

---

## Code Style

### Formatter & Linter

- **Formatter**: `ruff format` (replaces Black; Black is kept in dev deps for editor compatibility)
- **Linter**: `ruff` with a strict, comprehensive rule set
- **Dependency manager**: `uv` — always use `uv add` / `uv remove` to manage packages

### Formatting Rules

| Rule | Value |
|---|---|
| Line length | **125** characters |
| Indent width | **4** spaces |
| Quote style | **double** quotes |
| Trailing commas | respected (`skip-magic-trailing-comma = false`) |
| Line ending | auto |
| Docstring code blocks | formatted (`docstring-code-format = true`) |

### Import Order (isort via ruff)

- Standard library → third-party → first-party (`config`) → local
- `force-sort-within-sections = true`
- `split-on-trailing-comma = true`, `combine-as-imports = true`
- Two blank lines after the import block (`lines-after-imports = 2`)

### Complexity Limits

| Metric | Limit |
|---|---|
| McCabe complexity | 10 |
| Max function arguments | 7 |
| Max branches | 12 |
| Max return statements | 6 |
| Max statements per function | 50 |

### Active Lint Rule Groups

`E/W` (pycodestyle) · `F` (pyflakes) · `C90` (mccabe) · `I` (isort) · `N` (pep8-naming) · `UP` (pyupgrade) · `S` (bandit security) · `BLE` (blind except) · `FBT` (boolean trap) · `B` (bugbear) · `A` (builtins shadow) · `C4` (comprehensions) · `DTZ` (timezone-aware datetimes) · `T20` (no print) · `PT` (pytest style) · `RET` (return) · `SIM` (simplify) · `ARG` (unused args) · `ERA` (no commented-out code) · `PL` (pylint) · `RUF` (ruff-specific)

### Per-file Exceptions

| Glob | Relaxed rules |
|---|---|
| `tests/**/*.py` | `S101` (assert), `ARG001/2`, `FBT001/2`, `PLR2004` (magic values), `S311` (random) |
| `config/settings/*.py` | `F401`, `F403` (wildcard re-exports intentional) |
| `manage.py` | `T201` (print allowed) |

### General Conventions

- No `print()` in production code — use `structlog` for all logging.
- All datetime objects must be timezone-aware (`DTZ` rules enforced).
- Boolean positional parameters in public APIs are forbidden (`FBT` rules).
- Avoid shadowing Python builtins (e.g. `id`, `type`, `list`).
- Do not leave commented-out code in committed files (`ERA001`).
- Migrations (`*/migrations/*`) are fully excluded from linting.

### Language Rules

| Context | Language |
|---|---|
| Code (variables, functions, classes, comments, docstrings) | English |
| API responses (`code`, `msg`, field names) | English |
| Web page UI copy and templates | English + Indonesian (Bahasa Indonesia) |
| Template variable names | English |

---

### Database & QuerySet Patterns

#### Avoid N+1 Queries

- Always use `select_related()` for ForeignKey / OneToOne lookups and `prefetch_related()` for reverse / M2M relations.
- Select only the fields you need with `.only()` or `.values()` / `.values_list()`. Do not fetch entire rows when a subset suffices.

#### Use QuerySet Managers

- If a query pattern is repeated more than once, extract it into a custom `QuerySet` method or a model `Manager`.
- Keep business logic in `services.py`, not in views or models. Models define data and managers; services orchestrate.

```python
# Preferred
class EmployeeQuerySet(models.QuerySet["Employee"]):
    def active(self) -> "EmployeeQuerySet":
        return self.filter(is_active=True)

class Employee(TimeStampedModel):
    objects = EmployeeQuerySet.as_manager()
```

#### Migrations

- One logical change per migration. Do not combine schema changes with data migrations.
- Always review auto-generated migrations before committing.

---
