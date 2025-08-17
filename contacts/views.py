from django.contrib import messages
from django.shortcuts import redirect, render

from common.tasks import send_contact_email
from contacts.forms import ContactForm

# Create your views here.


def contact(request):
    """
    Render the contact page.
    """
    if request.method == "POST":
        # Handle form submission logic here
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send the contact email from the task file
            send_contact_email(contact)
            messages.success(request, "Your message has been sent successfully.")
            return redirect("home")
        else:
            messages.error(request, "There was an error sending your message.")
    else:
        form = ContactForm()

    context = {
        "page_title": "Contact",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Contact", "url": "Contact"},
        ],
        "form": form,
    }
    return render(request, "contacts/contact.html", context)
