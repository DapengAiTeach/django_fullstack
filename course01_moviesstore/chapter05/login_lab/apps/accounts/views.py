from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from apps.accounts.forms import LoginForm

def login_view(request):
    """
    ✅ authenticate / login 讲解重点：

    1) authenticate(request, username, password)
       - 只负责“校验账号密码”
       - 校验成功返回 User 对象；失败返回 None

    2) login(request, user)
       - 把 user 的身份写入 Session（服务器端）
       - 浏览器得到 sessionid（Cookie）
       - 之后每次请求都能通过 sessionid 找回用户 => request.user 生效

    3) 登录成功后跳转：
       - 优先跳转 next 参数（从 LOGIN_URL 重定向来的）
       - 没有 next 才使用 LOGIN_REDIRECT_URL
    """
    if request.user.is_authenticated:
        return redirect("movies:profile")

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

        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)

        return redirect("movies:profile")  # ✅ 对应 LOGIN_REDIRECT_URL

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    """
    ✅ logout 讲解重点：
    - logout(request) 会清空会话相关信息
    - request.user 变回 AnonymousUser
    - 退出后跳转使用 LOGOUT_REDIRECT_URL
    """
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("movies:home")