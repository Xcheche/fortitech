from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.models import Dashboard
from common.tasks import send_welcome_emails
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            # Get user by email using email as username
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        

# # Create new dashboard automatically with signal for social authentication
def create_dashboard(_backend, user, *_args, **_kwargs):
    if user:  # Ensure user exists
        try:
            with transaction.atomic():
                dashboard, created = Dashboard.objects.get_or_create(
                    user=user,
                    
                )
                #Send welcome email
                send_welcome_emails(user=user)
                if created:
                    logger.info("Created dashboard for user %s", user.pk)
        except Exception as e:
            logger.error(f"Error creating dashboard for social auth user: {e}")
