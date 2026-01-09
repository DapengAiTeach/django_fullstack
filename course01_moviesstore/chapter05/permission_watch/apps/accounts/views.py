from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from apps.accounts.forms import LoginForm

def user_login(request):
    """
    ✅ 认证：把匿名用户变成“已登录用户”
    - authenticate：验证用户名密码
    - login：写入 session，后续 request.user 才是一个真实 User
    """
    if request.user.is_authenticated:
        return redirect("movies:perm_dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            messages.success(request, "登录成功！")
            next_url = request.GET.get("next") or "movies:perm_dashboard"
            return redirect(next_url)

        messages.error(request, "用户名或密码错误")

    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("movies:perm_dashboard")