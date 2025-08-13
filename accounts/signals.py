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


@receiver(post_save, sender=User)
def create_user_dashboard(sender, instance, created, **kwargs):
    """
    Creates a Dashboard object and sends a welcome email when a new user is created.
    """
    if created:
        # Create the dashboard
        dashboard = Dashboard.objects.create(user=instance)

        # Send an email
        # send_mail(
        #     subject='Welcome to My Cypher Guard Dashboard',
        #     message=f'Hi {instance.email}, your dashboard has been created successfully! Feel free to edit your dashboard.',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[instance.email],
        #     fail_silently=False,
        # )
        # from tasks.py
        send_welcome_emails(user=instance)

        # Optional: Set a default profile picture if it's not handled elsewhere
        default_image_path = os.path.join(
            settings.BASE_DIR, "static", "images", "default.png"
        )
        if os.path.exists(default_image_path):
            with open(default_image_path, "rb") as f:
                dashboard.profile_picture.save("default.png", File(f), save=True)


# # myapp/signals.py
# import os
# # Correct import for File from Django's core files
# from django.core.files import File
# from django.contrib.auth import get_user_model
# from django.contrib.auth.signals import user_logged_in
# from django.db.models.signals import dashboard_save
# from django.dispatch import receiver
# from common.tasks import send_email
# from django.conf import settings

# # Import your custom Dashboard model
# from .models import Dashboard

# User = get_user_model()

# @receiver(user_logged_in)
# def send_welcome_email(sender, request, user, **kwargs):
#     """
#     Sends a welcome email to the user when they log in for the first time.
#     """
#     if user.last_login is None:
#         subject = "Welcome to your new dashboard!"
#         email_to = [user.email]
#         html_template = "email/welcome_email.html"
#         context = {"user": user}

#         send_email(subject, email_to, html_template, context)


# @receiver(dashboard_save, sender=User)
# def create_dashboard_and_set_default_image(sender, instance, created, **kwargs):
#     """
#     Creates a new Dashboard object, sets the default profile picture,
#     and sends a notification email to the admin.
#     """
#     if created:
#         # Step 1: Create a new Dashboard object for the new user
#         dashboard = Dashboard.objects.create(user=instance)

#         # Step 2: Define the path to your default image in the static folder
#         default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default.png')

#         # Step 3: Check if the file exists and save it to the ImageField
#         if os.path.exists(default_image_path):
#             with open(default_image_path, 'rb') as f:
#                 # Save the default image, which copies it to the media folder
#                 dashboard.profile_picture.save('default.png', File(f), save=True)

#         # Step 4: Send the notification email to the admin
#         subject = "New Account Signed Up!"
#         owner_emails = ["owner@example.com", "checheomenife@gmail.com"]
#         html_template = "email/owner_notification.html"
#         context = {"user_email": instance.email}

#         send_email(subject, owner_emails, html_template, context)
