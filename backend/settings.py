import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-a_!w^tnqqyut9-uhr#-$vx*v*24gtw)yzt*gb!*sx993ur-+1l"

env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "accounts.CustomUser"

INSTALLED_APPS = [
    "accounts",
    "base",
    "contacts",
    "tailwind",
    "theme",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = ["127.0.0.1"]

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

if DEBUG:

    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:

    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"  # URL to access static files

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # So Django can find Tailwind CSS
]

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)  # Where collectstatic will collect static files for production

# Media files (User uploaded content)
MEDIA_URL = "/media/"  # URL to access media files

MEDIA_ROOT = BASE_DIR / "media"  # Folder where uploaded media files will be saved

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
