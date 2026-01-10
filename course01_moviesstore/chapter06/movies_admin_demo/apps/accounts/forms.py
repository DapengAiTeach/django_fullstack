from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    """
    注册表单：用于前台演示 Bootstrap 表单交互。
    注意：生产环境要加邮箱验证/验证码/密码强度策略等。
    """
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("两次密码不一致")
        return cleaned


class LoginForm(AuthenticationForm):
    """
    Django 自带 AuthenticationForm：我们直接用它，教学更标准。
    """
    pass