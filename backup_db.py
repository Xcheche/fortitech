
import os
import subprocess
from datetime import datetime, timedelta
import sys

PROJECT_PATH = "/home/cheche/Documents/django_projects/fortitech/"
BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"db_backup_{timestamp}.json"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Determine which environment you are backing up:
# For local backup set 'local', for production set 'prod'
env = os.getenv('ENV', 'local')  # Default to local if ENV var not set

settings_module = "config.settings.prod" if env == "prod" else "config.settings.local"

command = [
    sys.executable,
    os.path.join(PROJECT_PATH, "manage.py"),
    "dumpdata",
    "--indent=2",
    f"--output={backup_path}",
    f"--settings={settings_module}",  # Specify settings here
]

env_vars = os.environ.copy()
env_vars["DJANGO_SETTINGS_MODULE"] = settings_module

try:
    subprocess.run(command, check=True, env=env_vars)
    print(f"Database backup successful: {backup_path}")
except subprocess.CalledProcessError as e:
    print(f"Error during database backup: {e}")
    sys.exit(1)



#To test for 3 minutes crontab -e switch django to True to pick local settings
#*/3 * * * * export ENV=local && cd /home/cheche/Documents/django_projects/fortitech/ && /home/cheche/Documents/django_projects/fortitech/.venv/bin/python backup_db.py >> backup.log 2>&1
#To set  for prod set django to True to pick prod settings
