# config/settings/base.py

from decouple import config, Csv

from pathlib import Path

from .storages import *  # noqa: F403
from .email_config import *  # noqa: F403
from .celery import *  # noqa: F403


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")


# Application definition


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    "cloudinary",
    "cloudinary_storage",
    "gunicorn",
]
PROJECT_APPS = [
    # Projects
    "accounts",
    "blog",
    "shop",
    "contacts",
]
THIRD_PARTY_APPS = [
    # External apps/packages
    "whitenoise",
    "ckeditor",
    "django_extensions",
    "social_django",
    # "django_password_eye",  for password visibility toggle
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
# Middleware
# https://docs.djangoproject.com/en/5.2/ref/settings/#middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.categories_with_post_count",
            ],
        },
    },
]


# Add social_django context processors
TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "social_django.context_processors.backends",
    "social_django.context_processors.login_redirect",
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# DATABASES normally not set here or set to empty dict if needed
DATABASES = {}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# WhiteNoise static files storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Upload path for ckeditor

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 700,
    }
}


# Default message storage (session storage)
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Customize message tags for Bootstrap compatibility

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-info",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger",
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Ensure the custom user model exists in accounts/models.py as class User(AbstractUser)
AUTH_USER_MODEL = "accounts.User"





#Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}





#------------------Social_django----------------
AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'accounts.authentication.EmailAuthBackend',
'social_core.backends.google.GoogleOAuth2',
'social_core.backends.github.GithubOAuth2',
] 


#-------------------------------Social Auth Pipeline------------------ 
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',       # must come first
    'accounts.pipeline.debug_user',                     # <-- add here
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


#-------- Google OAuth2------------------------------
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_FORCE_EMAIL_VALIDATION = True

# ❗ CRITICAL — ADD THIS
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    "prompt": "select_account",
    "access_type": "offline"
}

# settings.py
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# If you deploy behind HTTPS (Render/Cloud Run/etc.), set these for prod:

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login-error/"
APPEND_SLASH = True


CSRF_TRUSTED_ORIGINS = ["https://www.fortitech9ja.com", "https://www.fortitech9ja.com"]

#Github OAuth2
SOCIAL_AUTH_GITHUB_KEY=config('GITHUB_OAUTH2_KEY')
SOCIAL_AUTH_GITHUB_SECRET=config('GITHUB_OAUTH2_SECRET')



LOGIN_REDIRECT_URL = '/'  # or wherever you want user to land after login

LOGIN_URL = "login"
LOGOUT_URL = "logout"


# Safety: fail loud if still missing (remove once set)
if not SOCIAL_AUTH_GITHUB_KEY or not SOCIAL_AUTH_GITHUB_SECRET:
    raise RuntimeError(
        "GitHub OAuth env vars missing. Set SOCIAL_AUTH_GITHUB_KEY/SECRET or GITHUB_OAUTH2_KEY/SECRET"
    )
