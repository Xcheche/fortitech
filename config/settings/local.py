from .base import *
from decouple import config, Csv

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")

# Use SQLite for local development to simplify if you want
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fortitech_local',
        'USER': 'cheche',
        'HOST': 'localhost',
        'PORT': '5432',
        # No password needed since PostgreSQL is configured with 'trust' authentication
        'PASSWORD': '',
    }
}


print(DATABASES)
