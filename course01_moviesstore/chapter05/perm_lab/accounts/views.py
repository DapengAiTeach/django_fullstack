from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import LoginForm

def user_login(request):
    """
    认证入口：登录后 request.user 才会变成真实用户
    """
    if request.user.is_authenticated:
        return redirect("accounts:me")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            messages.success(request, "登录成功！")
            return redirect("accounts:me")
        messages.error(request, "用户名或密码错误")

    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("movies:movie_list")

@login_required
def me(request):
    """
    ✅ 三大核心模型可视化页面（教学核心）
    - User：用户结构（username/is_staff/is_superuser/...）
    - Group：角色（request.user.groups）
    - Permission：权限（user_permissions + group.permissions）
    - 合并机制：has_perm 是最终裁决
    """
    user = request.user

    # 1) 用户加入的角色（Group）
    groups = user.groups.all()

    # 2) 用户“直接”拥有的权限（ManyToMany -> auth_permission）
    direct_perms = user.user_permissions.all()

    # 3) 用户通过角色获得的权限（把每个 group 的 permissions 拉出来）
    group_perms = []
    for g in groups:
        group_perms.extend(list(g.permissions.all()))

    # 4) 最终权限判定：Django 用 has_perm 做“合并后的最终判定”
    #    这里选几个典型权限给页面演示（是否生效）
    demo_codes = [
        "movies.add_movie",
        "movies.change_movie",
        "movies.delete_movie",
        "movies.view_movie",
        "movies.publish_movie",
        "movies.export_movie",
    ]
    demo_results = [(code, user.has_perm(code)) for code in demo_codes]

    return render(request, "accounts/me.html", {
        "groups": groups,
        "direct_perms": direct_perms,
        "group_perms": group_perms,
        "demo_results": demo_results,
    })
