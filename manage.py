#!/usr/bin/env python
import os
import sys
from decouple import config

def main():
    debug = config('DEBUG', default=False, cast=bool)
    print("DEBUG value from .env or environment:", debug)
    if debug:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
        print("Using settings module:", os.environ.get('DJANGO_SETTINGS_MODULE'))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()


