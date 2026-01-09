from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from apps.accounts.forms import LoginForm

def login_view(request):
    """
    ✅ 未登录用户重定向流程（课堂最容易讲清楚）：

    - 用户访问 /vip/（受保护）
    - login_required 返回 302 -> /accounts/login/?next=/vip/
    - 登录成功后：
        1) 如果存在 next，就优先 redirect(next)
        2) 否则 redirect(LOGIN_REDIRECT_URL)
    """
    if request.user.is_authenticated:
        return redirect("movies:vip")

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

        # ✅ next 参数：把用户送回“原本想去的页面”
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)

        # ✅ 没有 next 才用默认跳转
        return redirect("movies:vip")

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("movies:home")