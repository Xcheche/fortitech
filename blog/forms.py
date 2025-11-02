# forms.py
from django import forms
from .models import Comment,Post, Category


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

#==================Comment form=====================
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


#=================================Post form=================




class PostForm(forms.ModelForm):
    # Nesting category model so it can show in ui in form of dropdown
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['slug', 'author','publish','views_count']  # Don't show slug and author in the user-facing form



# Non model form for sharing post
class SharePostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)