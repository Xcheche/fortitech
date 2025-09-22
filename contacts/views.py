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
            # Check form purpose, if register course redirect to courses page
            if form.cleaned_data["purpose"] == "register_course":
                return redirect(
                    "register_course"
                )  # Assuming you have a URL named 'courses'
            else:
                # Send the contact email from the task file
                send_contact_email(contact)
                messages.success(request, "Your message has been sent successfully.")
                return redirect("home")
        else:
            messages.error(request, "There was an error sending your message.")
    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, "contacts/contact.html", context)


def register_course(request):
    return render(request, "contacts/register_course.html")
