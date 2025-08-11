from django.shortcuts import render

# Create your views here.


def contact(request):
    """
    Render the contact page.
    """

    context = {
        "page_title": "Contact",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Contact", "url": "Contact"},
        ],
    }
    return render(request, "contacts/contact.html", context)
