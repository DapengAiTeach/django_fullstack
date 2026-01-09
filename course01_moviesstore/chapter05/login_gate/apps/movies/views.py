from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    """
    首页：提供入口，让学生去点“VIP 页面”，观察未登录重定向流程。
    """
    return render(request, "movies/home.html")

@login_required
def vip(request):
    """
    ✅ @login_required 工作原理（课堂讲解重点）：

    1) login_required 会检查 request.user.is_authenticated
       - True：放行，执行 vip 视图
       - False：直接返回一个 302 重定向响应

    2) 重定向去哪里？
       - 去 settings.LOGIN_URL 指定的登录地址（本例 accounts:login）

    3) next 参数怎么来的？
       - login_required 会把用户“原本想访问的路径”拼到 ?next=... 上
       - 例如：/vip/ -> /accounts/login/?next=/vip/
    """
    return render(request, "movies/vip.html")

@login_required
def next_debug(request):
    """
    一个辅助页面：把当前请求路径与登录状态展示出来，便于课堂演示。
    """
    return render(request, "movies/next_debug.html", {
        "path": request.path,
        "is_auth": request.user.is_authenticated,
        "username": request.user.username,
    })