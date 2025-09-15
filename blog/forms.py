# forms.py
from django import forms
from .models import Comment

BAD_WORDS = [
    "badword1",
    "badword2",
    "stupid",
    "idiot",
    "sex",
    "rape",
    "kill",
    "fool",
    "thief",
    "scammer",
    "animal",
    "monkey",
    "ugly",
    "pig",
]  # extend this list


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

    def clean_body(self):
        body = (
            super().clean_body()
            if hasattr(super(), "clean_body")
            else self.cleaned_data.get("body", "")
        )
        for word in BAD_WORDS:
            if word.lower() in body.lower():
                raise forms.ValidationError(
                    "Your comment contains inappropriate language."
                )
        return body
