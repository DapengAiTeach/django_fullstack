from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from apps.accounts.forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect("movies:vip_cbv")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            messages.error(request, "用户名或密码错误")
            return render(request, "accounts/login.html", {"form": form})

        login(request, user)
        messages.success(request, "登录成功！")

        # ✅ CBV 受保护页跳过来会带 next
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)

        return redirect("movies:vip_cbv")

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("movies:home")