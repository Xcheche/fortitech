from django.shortcuts import render

# Create your views here.


def home(request):

    context = {
        "page_title": "Home",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},  # The current page is 'Home'
            {"name": "Home", "url": "Home"},
        ],
    }
    return render(request, "blog/index.html", context)
