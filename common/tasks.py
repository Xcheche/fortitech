

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags


from django.conf import settings

from common.utils.thread_email import EmailThread


def send_email(subject: str, email_to: list[str], html_template, context):
    html_template = get_template(html_template)
    html_content = html_template.render(context)

    # Create a plain text version from the HTML content
    text_content = strip_tags(html_content)


   # Create the email message with both plain text and HTML parts
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Set the plain text as the main body
        from_email="williams@fortitech9ja.com",
        to=email_to,
    )
    msg.attach_alternative(html_content, "text/html")
    # msg.send(fail_silently=False)
    EmailThread(msg).start()
#-----------------------------------------------------------------------------------------------------------------

# =====Welcome email for signal
# =========================================
#Not in use
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
    owner_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Send the welcome email to the new user
        send_email(
            subject="Welcome to Fortitech!",
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


# ============contact form email=========
# ========================================


def send_contact_email(contact):
    """
    Sends a contact form submission email:
    - One email goes to the site owner.
    - One confirmation email goes to the client.
    """

    # 🔹 Site owner's email
    owner_email = "williams@fortitech9ja.com"

    try:
        # === 1) Send email to OWNER ===
        owner_context = {"contact": contact}
        owner_html = render_to_string("emails/contact_owner.html", owner_context)

        owner_subject = "📩 New Contact Form Submission"
        owner_email_message = EmailMultiAlternatives(
            subject=owner_subject,
            body=owner_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[owner_email],
        )
        owner_email_message.attach_alternative(owner_html, "text/html")
        #owner_email_message.send()
        EmailThread(owner_email_message).start()

        # === 2) Send confirmation email to CLIENT ===
        client_context = {"contact": contact}
        client_html = render_to_string("emails/contact_client.html", client_context)

        client_subject = "✅ Thanks for contacting us"
        client_email_message = EmailMultiAlternatives(
            subject=client_subject,
            body=client_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact.email],  # assumes your model has "email" field
        )
        client_email_message.attach_alternative(client_html, "text/html")
        # client_email_message.send()
        EmailThread(client_email_message).start()

        print("Both owner and client emails sent successfully.")

    except Exception as e:
        print(f"Error sending contact emails: {e}")

    """
    Sends a contact form submission email to the site owner.
    """
    # Define the context for the contact email
    context = {
        "contact": contact,
    }

    # Replace with the actual email of your site owner
    owner_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_email(
            subject="New Contact Form Submission",
            email_to=[owner_email],
            html_template="emails/contact_owner.html",
            context=context,
        )
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error sending contact email: {e}")
