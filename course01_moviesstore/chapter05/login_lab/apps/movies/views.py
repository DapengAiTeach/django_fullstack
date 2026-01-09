from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

def home(request):
    """
    ✅ 首页：展示登录状态与入口
    """
    return render(request, "movies/home.html")

@login_required
def profile(request):
    """
    ✅ 个人中心：必须登录才能访问
    - 未登录会被重定向到 LOGIN_URL
    - 并自动携带 next=/profile/
    """
    return render(request, "movies/profile.html")

@login_required
def session_debug(request):
    """
    ✅ Session 演示页（课堂非常好用）：
    - 这里手动写入 session，并展示它确实能跨请求保存
    """
    # 写入 session：模拟你在业务中记录“访问次数”
    count = request.session.get("visit_count", 0)
    request.session["visit_count"] = count + 1

    # 写入 session：模拟记录“最后访问时间”
    request.session["last_seen"] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    ctx = {
        "visit_count": request.session["visit_count"],
        "last_seen": request.session["last_seen"],
        "session_key": request.session.session_key,  # session 的唯一标识
    }
    return render(request, "movies/session_debug.html", ctx)