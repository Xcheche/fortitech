# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import get_template


# def send_email(subject: str, email_to: list[str], html_template, context):
#     msg = EmailMultiAlternatives(
#         subject=subject, from_email="noreply@example.com", to=email_to
#     )
#     html_template = get_template(html_template)
#     html_content = html_template.render(context)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send(fail_silently=False)

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags


from django.conf import settings


def send_email(subject: str, email_to: list[str], html_template, context):
    html_template = get_template(html_template)
    html_content = html_template.render(context)

    # Create a plain text version from the HTML content
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Set the plain text as the main body
        from_email="noreply@example.com",
        to=email_to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


# =====Welcome email for signal
def send_welcome_emails(user):
    """
    Sends a welcome email to a new user and a notification email to the site owner.
    """
    # Ensure the user object has an email attribute
    user_email = getattr(user, "email", None)
    if not user_email:
        raise ValueError("User object must have a valid 'email' attribute.")

    # Define the context for the user's welcome email
    user_context = {
        "user": user,
    }

    # Define the context for the owner's notification email
    owner_context = {
        "new_user": user,
    }

    # Replace with the actual email of your site owner
    owner_email = "cypherguard@example.com"

    try:
        # Send the welcome email to the new user
        send_email(
            subject="Welcome to  Cypher Guard ",
            email_to=[user_email],
            html_template="emails/welcome.html",
            context=user_context,
        )

        # Send the notification email to the site owner
        send_email(
            subject=f"New User Registered: {user_email}",
            email_to=[owner_email],
            html_template="emails/owneremail.html",
            context=owner_context,
        )
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error sending welcome emails: {e}")
