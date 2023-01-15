import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

# settings modules
include(
    "components/apps.py",
    "components/database.py",
    "components/middleware.py",
    "components/password_validation.py",
    "components/templates.py",
    "components/custom_logger.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "172.18.0.1", "localhost"]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["app/movies/locale"]

INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
]

CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0:80",
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8080",
]
