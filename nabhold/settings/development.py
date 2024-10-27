# nabhold/settings/development.py
from decouple import config
from .base import *

#DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = config("DEBUG", default=True, cast=bool)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"
