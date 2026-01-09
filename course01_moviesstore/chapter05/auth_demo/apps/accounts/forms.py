from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


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

    error_messages = {
        "username_exists": "该账号已存在，请更换。",
        "username_invalid": "账号仅支持字母、数字或下划线。",
        "username_length": "账号长度需为 3-20 位。",
        "password_mismatch": "两次输入的密码不一致。",
    }

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            raise ValidationError(self.error_messages["username_invalid"])
        if not (3 <= len(username) <= 20):
            raise ValidationError(self.error_messages["username_length"])
        if User.objects.filter(username=username).exists():
            raise ValidationError(self.error_messages["username_exists"])
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="账号",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入账号"}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
    )

    error_messages = {
        "invalid_login": "账号或密码错误。",
        "inactive": "该账号已被停用。",
    }
