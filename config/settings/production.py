import dj_database_url
from .base import *
from decouple import config, Csv


ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="*")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DATABASE_NAME"),
#         "USER": config("DATABASE_USER"),
#         "PASSWORD": config("DATABASE_PASSWORD"),
#         "HOST": config("DATABASE_HOST"),
#         "PORT": config("DATABASE_PORT"),
#         "CONN_MAX_AGE": 0,  # important for serverless: close connection per request
#         "OPTIONS": {
#             "sslmode": config("DATABASE_SSLMODE", default="require"),
#         },
#     }
# }

#Database url

DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL"),
        conn_max_age=0,     # serverless safe
        ssl_require=True    # Neon requires SSL
    )
}

print(DATABASES)
