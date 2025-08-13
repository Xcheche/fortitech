from django import forms
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError

from .models import *


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # You can add other fields from CustomUser here
        fields = ["email"]
        exclude = ["user"]  # Prevents 'user' from showing up in the form


class DashboardUpdateForm(forms.ModelForm):
    # This form handles the country and city fields
    # You might want to override the city field to make it a simple ChoiceField
    # for the initial form render before JavaScript takes over.

    class Meta:
        model = Dashboard
        # fields = "__all__"
        exclude = ["user"]

    def clean_post_code(self):
        post_code = self.cleaned_data.get("post_code")
        if post_code:
            # Check if the zip code contains only alphanumeric characters
            if not all(c.isalnum() or c.isspace() for c in post_code):
                raise forms.ValidationError(
                    "Postal code must contain only letters and numbers."
                )
        return post_code
