"""
Django base settings for HR Management System.

This module integrates configuration from:
- envcommon.py: Environment-specific settings (development/production)
- databases.py: Database configuration (SQLite/PostgreSQL)
- compconfig.py: Company profile from YAML
- factory.py: Dependency injection for configuration assembly

Configuration is built using Pydantic Settings and dependency-injector.
"""

import os

from .factory import get_settings_dict

# Determine environment from environment variable
ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

# Build configuration using dependency injection
_config = get_settings_dict(environment=ENVIRONMENT)

# Core Settings
BASE_DIR = _config["base_dir"]
SECRET_KEY = _config["secret_key"]
DEBUG = _config["debug"]
ALLOWED_HOSTS = _config["allowed_hosts"]

# Database Configuration
DATABASES = _config["databases"]

# Company Configuration (from YAML)
COMPANY_PROFILE = _config["company"]
COMPANY_NAME = COMPANY_PROFILE["name"]
COMPANY_LEGAL_NAME = COMPANY_PROFILE["legal_name"]
COMPANY_DESCRIPTION = COMPANY_PROFILE["description"]
COMPANY_INDUSTRY = COMPANY_PROFILE["industry"]
COMPANY_EMAIL = COMPANY_PROFILE["contact"]["email"]
COMPANY_PHONE = COMPANY_PROFILE["contact"]["phone"]
COMPANY_WEBSITE = COMPANY_PROFILE["contact"]["website"]
COMPANY_TIMEZONE = COMPANY_PROFILE["business_hours"]["timezone"]
COMPANY_CURRENCY = COMPANY_PROFILE["hr_settings"]["default_currency"]

# Company context for templates
COMPANY_CONTEXT = _config["company_context"]

# Internationalization
LANGUAGE_CODE = _config["language_code"]
TIME_ZONE = COMPANY_TIMEZONE  # Use company timezone from YAML
USE_I18N = _config["use_i18n"]
USE_TZ = _config["use_tz"]

# Environment Flags
IS_DEVELOPMENT = _config["is_development"]
IS_PRODUCTION = _config["is_production"]

# Application Definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "django_extensions",
    "django_filters",
    # Local apps will be added here
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# Templates Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# HR Settings (from Company Profile)
HR_WORKING_HOURS_PER_WEEK = COMPANY_PROFILE["hr_settings"]["working_hours_per_week"]
HR_PROBATION_PERIOD_DAYS = COMPANY_PROFILE["hr_settings"]["probation_period_days"]
HR_ANNUAL_LEAVE_DAYS = COMPANY_PROFILE["hr_settings"]["annual_leave_days"]
HR_SICK_LEAVE_DAYS = COMPANY_PROFILE["hr_settings"]["sick_leave_days"]
HR_PAYROLL_CYCLE = COMPANY_PROFILE["hr_settings"]["payroll_cycle"]

# Company Departments
COMPANY_DEPARTMENTS = COMPANY_PROFILE["departments"]

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Static Files Configuration
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

# Media Files Configuration
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Configuration (if needed)
CORS_ALLOWED_ORIGINS = _config.get("cors_allowed_origins", [])

# Security Settings for Production
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
