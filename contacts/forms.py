from datetime import timedelta
from django.utils import timezone
from django import forms

from contacts.models import Contact


class ContactForm(forms.ModelForm):

    # form fields
    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "message", "purpose"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise forms.ValidationError("Enter a valid email address.")
        if len(email) > 254:
            raise forms.ValidationError(
                "Email address is too long. Maximum length is 254 characters."
            )
        one_hour_ago = timezone.now() - timedelta(hours=1)
        if Contact.objects.filter(email=email, created_at__gte=one_hour_ago).exists():
            raise forms.ValidationError(
                "You already messaged. Please wait at least 1 hour before sending another message."
            )
        return email

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if not message:
            raise forms.ValidationError("Message is required.")
        return message
