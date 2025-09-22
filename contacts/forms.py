from datetime import timedelta
from django.utils import timezone
from django import forms

from contacts.models import Contact


class ContactForm(forms.ModelForm):

    # form fields
    class Meta:
        """
        Meta class for the Contact form.

        Attributes:
            model (Contact): Specifies the model associated with the form.
            fields (list): List of fields to include in the form: "name", "phone", "email", "message", and "purpose".
        """
        model = Contact
        fields = ["name", "phone", "email", "message", "purpose"]
        







    def clean_email(self):
        """
        Validates the email field in the contact form.

        - Ensures the email is provided.
        - Checks for a valid email format (contains '@' and a '.' after '@').
        - Verifies the email does not exceed 254 characters.
        - Prevents sending another message from the same email within 1 hour.

        Raises:
            forms.ValidationError: If any validation fails.

        Returns:
            str: The validated email address.
        """
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
        """
        Validates the 'message' field in the form.

        Raises:
            forms.ValidationError: If the 'message' field is empty.

        Returns:
            str: The validated message.
        """
        message = self.cleaned_data.get("message")
        if not message:
            raise forms.ValidationError("Message is required.")
        return message
