# Project Overview (HR MS - Human Resource Management System)

- Framework → Django 6.0 (ASGI)
- Language → Python 3.14+
- Environment Configuration → pydantic + pydantic-settings with Structlog YAML
- Dependency Management → uv with pyproject.toml
- Database → Development: SQLite, Production: PostgreSQL
- API Layer → Django Rest Framework (DRF) with drf-spectacular
- Auth System → Django Auth with Custom User Model
- Token Auth → drf-simplejwt
- Permission Layer → Django Permission with Custom Policy Layer
- Task Queue → Celery with Celery-beat
- Testing → pytest, pytest-django, pytest-cov, with factory-boy + faker for test data generation
- Formatting → Ruff and Black, with MyPy for Type Checking (Optional)
- Secret Management → env Variables
- Static Handling → whitenoise
- ASGI → Gunicorn (Uvicorn)
- Logging → Structlog with JSON output
- Frontend → Django Templates with HTMX and AlpineJS

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
The following rules define the coding standards and engineering discipline for HR‑MS development. Only the sections below are considered the active development standards for the current phase. Adherence to these guidelines is mandatory for all contributors. These rules are enforced through automated tools (Ruff) and code reviews.

### General Principles
- **Consistency**: Follow the defined style rules consistently across the codebase to ensure readability and maintainability.
- **Clarity**: Write code that is clear and self-explanatory. Use descriptive variable and function names, and include comments where necessary to explain complex logic.
- **Simplicity**: Avoid unnecessary complexity. Write straightforward code that accomplishes the task without over-engineering.
- **Performance**: Write efficient code, but not at the expense of readability. Optimize only when there is a demonstrated need.
- **Security**: Follow best practices for secure coding, especially when handling user input, authentication, and sensitive data.
- Business logic must remain deterministic and testable. Avoid side effects and reliance on external state. 

### General Restrictions
- No `print()` statements in production code — use `structlog` for all logging.
- All datetime objects must be timezone-aware (`DTZ` rules enforced).
- Boolean positional parameters in public APIs are forbidden (`FBT` rules).
- Avoid shadowing Python builtins (e.g. `id`, `type`, `list`).
- Do not over-comment obvious code, but do include comments for complex or non-obvious logic.
- Do not leave commented-out code in committed files (`ERA001`).
- No Circular imports. Structure code to avoid circular dependencies between modules.
- No Hidden Side Effects. Functions and methods should not have hidden side effects that are not clear from their name or signature.

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
- Keep business logic in `services.py`, not in views or models. Models define data and managers; services orchestrate. All complex queries must live in the **selectors layer**.
- Avoid ORM calls directly inside views
- Queries must be index-aware for PostgreSQL (e.g., filter on indexed fields, avoid functions on indexed columns in filters).
- Keep queries composable
- Avoid loading large QuerySets into memory; use pagination or streaming when necessary.

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

### Django REST Framework (DRF) Patterns
#### Guidelines:
- Use **ViewSets with routers** for APIs
- Use **serializers for validation and transformation**
- Services perform business logic

#### Request flow:
```
request → serializer → service → response
```

#### Serializer responsibilities:
- input validation
- data transformation

#### Restrictions:
- Serializers must not implement business workflows
- Views must remain orchestration layers

Example:
```python
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
```

### Config and Env (Pydantic & Pydantic‑Settings)
Configuration must be **typed and validated**. Guidelines:
- All environment variables must be defined in **Pydantic settings models**
- Configuration must be centralized
- Do not call `os.getenv()` directly in application code
- All environment access must go through the settings layer (e.g., `from config.settings import settings`)
- Use `pydantic-settings` for hierarchical settings management (e.g., `BaseSettings` with nested models)

```python
from pydantic_settings import BaseSettings
class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str
class Settings(BaseSettings):
    database: DatabaseSettings
settings = Settings()
```

### Testing Patterns
- Use `pytest` with `pytest-django` for testing
- Use `factory-boy` and `faker` for test data generation (factories.py)
- Test structure: unit tests for models, serializers, and services; integration tests for views and API endpoints
- Use fixtures for common test setup (e.g., creating test users, setting up test databases)
- Test Coverage: Aim for ≥ 50% coverage on all new code. Use `pytest-cov` to measure and report coverage.

```python
# Example of a pytest fixture for creating a test user
@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="password")
```

### Logging Patterns
- Use `structlog` for structured logging with JSON output
- Log at appropriate levels (DEBUG for development, INFO for production, WARNING/ERROR for issues)
- Include relevant context in log messages (e.g., user ID, request path, correlation ID)

```python
import structlog
logger = structlog.get_logger(__name__)
logger.info("User logged in", user_id=user.id, path=request.path)
```

- Log important business events
- Log errors with contextual metadata
- Avoid logging sensitive information (e.g., passwords, personal data)

### Auth User Model Patterns
The system must define a custom Django User model from the start. This allows for future extensibility (e.g., adding fields like `employee_id`, `role`, etc.) without needing a disruptive migration later. Guidelines:
- Define a custom User model that inherits from `AbstractBaseUser` and `PermissionsMixin`
- Use `BaseUserManager` for user creation logic
- Include fields relevant to the HR domain (e.g., `employee_id`, `role`, `is_active`)

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
```

### Views and URL (Rules & Preference)
- Use **class-based views** (CBVs) for all views, even simple ones. This ensures consistency and makes it easier to add functionality later.
- Use **DRF ViewSets** for API endpoints, with routers for URL configuration.
- Keep views thin; they should only handle request parsing, response formatting, and orchestration. All business logic must be delegated to services.
- Use **Django's URL dispatcher** with `path()` and `include()` for clean URL configuration. Avoid hardcoding URLs in views; use `reverse()` or `reverse_lazy()` for URL resolution.

```python
# Example of a class-based view
from django.views import View
class EmployeeListView(View):
    def get(self, request):
        employees = get_all_employees()  # delegate to selector
        return JsonResponse({"employees": list(employees.values())})
```

### Templates Guidelines
- Use **Django templates** for server-side rendering of HTML pages.
- Use **HTMX** for dynamic, partial page updates without full reloads.
- Use **AlpineJS** for simple client-side interactivity (e.g., toggling visibility, handling form interactions).
- Keep templates simple and focused on presentation. Avoid complex logic in templates; use template tags or filters for any necessary logic.

```html
<!-- Example of a Django template with HTMX and AlpineJS -->
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle Details</button>
    <div x-show="open" hx-get="{% url 'employee-details' employee.id %}" hx-target="#details">
        <!-- Employee details will be loaded here -->
    </div>
</div>
```

- Template Partials will be stored in Components dir
- maintain clean HTML structure
- Use template inheritance for common layouts
- Semantic Titles and Labels (Don't use generic <div>, use <nav>, <header>, <main>, etc.) Based on the context of the content. This improves accessibility and SEO.

### Module Internal Structure
Each domain module should follow a consistent internal structure. 

modules/employee/

├── admin.py
├── apps.py
├── models.py
├── services.py
├── selectors.py
├── serializers.py
├── views.py
├── urls.py
├── managers.py
├── constants.py
├── migrations/
└── tests/

### Dependency Rules
- All external dependencies must be added via `uv add` and listed in `pyproject.toml`.
- Avoid adding unnecessary dependencies; prefer standard library and built-in Django features when possible.
- Keep dependencies up to date and monitor for security vulnerabilities.
- Use `uv update` regularly to keep dependencies current, but always review changelogs for breaking changes before updating.
- For frontend dependencies (e.g., HTMX, AlpineJS), use CDN links or include them in the static assets directory, but do not add them to `pyproject.toml`.

### Module Dependency Rules
- Modules should not have circular dependencies. If two modules need to interact, they should do so through well-defined interfaces (e.g., services or APIs).
- Shared utilities should be placed in the `shared/` directory and should not depend on any specific module.
- The `config/` module can be imported by any other module, but it should not import from other modules to avoid circular dependencies.
- Each module should be as self-contained as possible, with clear boundaries and minimal coupling to other modules.

- `auth` provides authentication primitives
- `user` defines login identity
- `employee` links HR data to users
- `organization` defines company hierarchy
- `employment` manages employment lifecycle

