# myapp/signals.py
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from common.tasks import send_email, send_welcome_emails
from .models import Dashboard

# Get the custom user model (if you have one)
User = get_user_model()
#-----logging setup-----
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)

def create_user_dashboard(sender, instance, created, **kwargs):
    
    """
    Creates a Dashboard object and sends a welcome email when a new user is created.
    Ensures the dashboard always has a default profile picture if none is set.
    """
    if created:
        dashboard = Dashboard.objects.create(user=instance)

        send_welcome_emails(user=instance)

        default_image_path = os.path.join(
            settings.BASE_DIR, "static", "images", "default.png"
        )

        #======= Only set the default profile picture if it's not already set=================
        if not dashboard.profile_picture:
            if os.path.exists(default_image_path):
               try:
                   with open(default_image_path, "rb") as f:
                       dashboard.profile_picture = File(f, name="default.png")
                       dashboard.save()  # Save the dashboard with the default image
               except Exception as e:
                   logger.error(f"Error setting default profile picture: {e}")