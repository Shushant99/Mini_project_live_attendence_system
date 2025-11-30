import os
from pathlib import Path

# BASE_DIR (use pathlib for clarity)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# For local development this is fine; in production use an environment variable.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-please-change")

# Set True for development; set False in production and set ALLOWED_HOSTS properly.
DEBUG = True

# When DEBUG=False, you MUST set ALLOWED_HOSTS to the hostnames/IPs that will serve the app.
# For local dev you can use:
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Minimal installed apps (add your apps below)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "attendance.apps.AttendanceConfig",
    "django.contrib.staticfiles",
    "rest_framework",         # if you installed DRF
    "attendance",             # your app
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

ROOT_URLCONF = "smart_attendance.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "smart_attendance.wsgi.application"

# Simple sqlite DB for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static / media (your existing snippet)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Session settings for "remember me"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7   # 7 days
SESSION_SAVE_EVERY_REQUEST = False

# Basic i18n/timezone defaults (you can change)
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/attendance/'
LOGIN_URL = '/accounts/login/'