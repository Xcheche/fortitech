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

def send_email(subject: str, email_to: list[str], html_template, context):
    html_template = get_template(html_template)
    html_content = html_template.render(context)
    
    # Create a plain text version from the HTML content
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject, 
        body=text_content,  # Set the plain text as the main body
        from_email="noreply@example.com", 
        to=email_to
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)