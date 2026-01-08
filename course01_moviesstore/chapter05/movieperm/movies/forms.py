# movies/forms.py
from django import forms
from movies.models import Movie

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"})
    )

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "year", "summary"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "例如：星际穿越"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "min": 1900, "max": 2100}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "写点剧情简介…"}),
        }