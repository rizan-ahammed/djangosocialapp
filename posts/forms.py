from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input"}), label="Tags (Comma separated)")

    class Meta:
        model = Post
        exclude = ("author", "published_date", "is_deleted", "categories")

        widgets = {
            "title": forms.TextInput(attrs={'class': "input"}),
            "short_description": forms.Textarea(attrs={'class': "input"}),
        }

        error_messages = {
            "title": {
                "required": "Title field is required",
            },
            "description": {
                "required": "Description field is required",
            },
            "short_description": {
                "required": "Short description field is required",
            },
            "featured_image": {
                "required": "Featured image field is required",
            },
            "is_draft": {
                "required": "Is draft field is required",
            },
            # "tags": {
            #     "required": "Tags field is required",
            # },
        }
