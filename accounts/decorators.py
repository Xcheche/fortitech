# Custom decorator

from django.http import HttpRequest
from django.shortcuts import redirect

# accounts/decorators.py

def redirect_authenticated_user(view_func):  # fixed spelling

    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper
