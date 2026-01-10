from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from apps.accounts.forms import RegisterForm, LoginForm

def home(request):
    return render(request, "movies/home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True  # ✅ 控制是否允许登录
            user.save()
            messages.success(request, "注册成功，请登录。")
            return redirect("movies:login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "登录成功！")
            return redirect("movies:home")
    else:
        form = LoginForm(request)
    return render(request, "accounts/login.html", {"form": form})