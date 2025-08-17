import os
import subprocess
from datetime import datetime, timedelta
import sys

# Path to your project's manage.py file  pwd to get the project path
# Adjust this path according to your project structure
# This is the path where your Django project is located
# Make sure to set this to the correct path where your manage.py file is located
PROJECT_PATH = "/home/cheche/Documents/django_projects/cypher-guard/"

# Path where you want to store backups
BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")

# Create the backups folder if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# --- BACKUP LOGIC ---

# Generate a filename with the current date and time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"db_backup_{timestamp}.json"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Construct the Django management command
command = [
    sys.executable,
    os.path.join(PROJECT_PATH, "manage.py"),
    "dumpdata",
    "--indent=2",
    f"--output={backup_path}",
]

# Run the command and save the backup
try:
    subprocess.run(command, check=True)
    print(f"Database backup successful: {backup_path}")
except subprocess.CalledProcessError as e:
    print(f"Error during database backup: {e}")
    sys.exit(1)  # Exit if backup fails to prevent accidental deletion of all files

# --- CLEANUP LOGIC ---

# Number of days to keep backups
DAYS_TO_KEEP = 7
# ==============for testing set to 1 hr below======
# 0.0416 represents 1 hour (1 / 24 hours) for testing
# DAYS_TO_KEEP = 0.0416
cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)

print(f"Cleaning up backups older than {DAYS_TO_KEEP} days...")

for filename in os.listdir(BACKUP_DIR):
    filepath = os.path.join(BACKUP_DIR, filename)
    # Check if the file is a backup and its modification time
    if os.path.isfile(filepath) and filename.startswith("db_backup_"):
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if mod_time < cutoff_date:
            try:
                os.remove(filepath)
                print(f"Deleted old backup: {filename}")
            except OSError as e:
                print(f"Error deleting file {filename}: {e}")

print("Cleanup complete.")


# =====crontab  instructions======== pwd for project path and which python to get the python path and virtual environment path
# crontab -e
# crontab -l  see all crontabs
# cd into project root path and merge with the python virtual environment path
#  Testing at every 3 minutes
#          */3 * * * * cd /home/cheche/Documents/django_projects/cypher-guard/ && /home/cheche/Documents/django_projects/cypher-guard/.venv/bin/python backup_db.py
# for production use 3am
#        0 3 * * * cd /home/cheche/Documents/django_projects/cypher-guard/ && /home/cheche/Documents/django_projects/cypher-guard/.venv/bin/python backup_db.py
