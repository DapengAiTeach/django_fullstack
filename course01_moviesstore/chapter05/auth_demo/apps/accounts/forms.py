from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="账号",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入账号"}),
    )
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请再次输入密码"}),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="账号",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入账号"}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
    )
