from django.urls import path
"""
URL configuration for the contacts app.

Defines the following routes:
- 'contact/': Maps to the 'contact' view, used for handling contact form submissions.
- 'register_course/': Maps to the 'register_course' view, used for course registration functionality.
"""
from . import views


urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("register_course/", views.register_course, name="register_course"),
]
