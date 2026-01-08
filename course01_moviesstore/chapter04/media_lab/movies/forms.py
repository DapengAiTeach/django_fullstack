from django import forms
from .models import Movie

class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description", "cover"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
