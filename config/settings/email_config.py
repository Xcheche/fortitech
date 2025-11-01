from .base import *  # noqa: F403
import os
from decouple import config

# ======== Email Configuration from Environment Variables======
debug = config("DEBUG", default=False, cast=bool)

if debug:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # for console
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # for smtp

#Email Smtp settings for  mailpit
EMAIL_HOST = config("EMAIL_HOST", default="localhost")  # Mailpit host
EMAIL_PORT = config("EMAIL_PORT", default=1025, cast=int)  # Mailpit SMTP port
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # No auth needed
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
#EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="williams@fortitech9ja.com")














#====================================== Email Smtp settings for  zoho mail========================================================

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = config("EMAIL_HOST", default="smtp.zoho.com")
# EMAIL_PORT = config("EMAIL_PORT", default=465, cast=int)
# EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="williams@fortitech9ja.com")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
# EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
# EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=True, cast=bool)
# DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="williams@fortitech9ja.com")
















# Debugging output to verify email settings are loaded correctly
print(
    "Email configuration loaded: ",
    {
        "EMAIL_BACKEND": EMAIL_BACKEND,
        "EMAIL_HOST": EMAIL_HOST,
        "EMAIL_PORT": EMAIL_PORT,
        "EMAIL_USE_TLS": EMAIL_USE_TLS,
        #"EMAIL_USE_SSL": EMAIL_USE_SSL,
    },
)
