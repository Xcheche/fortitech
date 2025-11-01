from .base import *  # noqa: F403
from decouple import config, Csv
import psycopg2  # noqa: F401

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")

#=====NOt in use now =====
#Use SQLite for local development to simplify if you want
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

#Database 2 -- Supabase Postgresql  for local development testing purpose only
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",  # Supabase default DB name
#         "USER": "postgres.cmxrwwzurbtrrjvhwhfd",  # your actual user
#         "PASSWORD": "fortitech2025",
#         "HOST": "aws-1-eu-west-2.pooler.supabase.com",
#         "PORT": "5432",  # 👈 switch to 5432
#         "OPTIONS": {
#             "sslmode": "require",  # 👈 force SSL
#         },
#     }
# }
# Django Debug Toolbar
INSTALLED_APPS += [ "debug_toolbar"]
# Additional middleware introduced by debug toolbar
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]



# Allow internal IPs for debugging
INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
    "0.0.0.1",
    "localhost",
    "testserver",
]

ALLOWED_HOSTS = INTERNAL_IPS
