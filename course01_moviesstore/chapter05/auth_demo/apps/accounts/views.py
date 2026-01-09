from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from .forms import LoginForm, RegisterForm

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("accounts:login")

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("home:home")
