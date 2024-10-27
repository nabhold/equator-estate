# nabhold/settings/production.py
from decouple import config
from .base import *


DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
