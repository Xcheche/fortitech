# # accounts/signals.py
# import os
# import logging
# from django.conf import settings
# from django.core.files import File
# from django.db import transaction
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Dashboard
# from common.tasks import send_welcome_emails

# logger = logging.getLogger(__name__)
# User = get_user_model()


# @receiver(post_save, sender=User)
# def create_user_dashboard(sender, instance, created, **kwargs):
#     """
#     Creates a Dashboard object and sends a welcome email when a new user is created.
#     Ensures the dashboard always has a default profile picture if none is set.
#     Safe for superuser creation.
#     """
#     if created:
#         try:
#             with transaction.atomic():
#                 # Get or create dashboard
#                 dashboard, created_dashboard = Dashboard.objects.get_or_create(user=instance)

#             # Send welcome email (safe outside transaction)
#             send_welcome_emails(user=instance)

#             # Only assign default profile picture if running in normal user creation
#             if not instance.is_superuser:
#                 default_image_path = os.path.join(settings.BASE_DIR, "static/images/default.png")
#                 if not dashboard.profile_picture and os.path.exists(default_image_path):
#                     try:
#                         with open(default_image_path, "rb") as f:
#                             dashboard.profile_picture = File(f, name="default.png")
#                             dashboard.save()
#                     except Exception as e:
#                         logger.error(f"Error assigning default profile picture: {e}")

#         except Exception as e:
#             logger.error(f"Error creating dashboard transaction: {e}")
