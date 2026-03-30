# HR-MS (Human Resource Management System)

## Overview

The Human Resource Management System (HR-MS) is a comprehensive web application built with Django that serves as a central repository for all employee information. This system is designed to streamline HR processes, improve data accuracy, and provide a solid foundation for future module integrations.

## Core Features

- **Employee Information Management**: Centralized database for personal and professional employee data.
- **Employment Details**: Track job titles, departments, reporting managers, and employment status.
- **Contract Management**: Manage employment contracts, including start/end dates and terms.
- **Salary Information**: Handle salary details, pay grades, and payment frequency.
- **Emergency Contacts**: Store emergency contact information for employees.
- **Organizational Structure**: Define departments and job titles within the company.

## Tech Stack

- **Backend**: Django 6.0 (ASGI)
- **Language**: Python 3.14+
- **API**: Django Rest Framework (DRF) with `drf-spectacular` for schema generation.
- **Authentication**: Django Auth with a custom User model and `drf-simplejwt` for token-based authentication.
- **Database**: PostgreSQL (production), SQLite (development).
- **Task Queue**: Celery with Celery Beat for asynchronous tasks.
- **Frontend**: Django Templates with HTMX and Alpine.js for dynamic UI.
- **Dependency Management**: `uv`
- **Testing**: `pytest`, `pytest-django`, `factory-boy`
- **Formatting & Linting**: `Ruff`, `Black`, `MyPy`

## Project Structure

The project is organized into several key directories:

- `applications/`: Contains individual Django apps for different business domains (e.g., `employee`, `attendance`).
- `config/`: Project-level configuration, including settings, URLs, and ASGI/WSGI entry points.
- `modules/`: Core Django apps like `user` and `auth`.
- `shared/`: Shared utilities and base models used across the project.
- `templates/`: Django HTML templates.
- `assets/`: Static files (CSS, JavaScript, images).
- `tests/`: Top-level integration and configuration tests.

## Getting Started

### Prerequisites

- Python 3.14+
- `uv` for dependency management
- PostgreSQL (for production)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd hr-ms
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use ` .venv\Scripts\activate`
    uv pip install -r requirements.txt
    uv pip install -r requirements-dev.txt
    ```

3.  **Configure environment variables:**

    Create a `.env` file in the root directory and populate it with the necessary settings (e.g., database credentials, secret key). Refer to `config/settings/envcommon.py` for required variables.

4.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## Running Tests

To run the test suite, use `pytest`:

```bash
pytest
```

To generate a coverage report:

```bash
pytest --cov=.
```

## Code Style & Linting

This project uses `Ruff` for linting and formatting. The configuration can be found in `pyproject.toml`.

To check for linting errors:

```bash
ruff check .
```

To format the code:

```bash
ruff format .
```

## Future Roadmap

- **Attendance Module**: Track employee attendance, leaves, and work hours.
- **Payroll Module**: Automate payroll calculation and processing.
- **HSE Module**: Manage Health, Safety, and Environment related incidents and training.
- **Man-Hours Module**: Track man-hours for specific projects or tasks.
- **Self-Service Portal**: Allow employees to view and manage their own information.
