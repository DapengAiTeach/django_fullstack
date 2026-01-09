from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.movies.models import Movie

def perm_dashboard(request):
    """
    ✅ 页面本身谁都能看（演示更友好）
    ✅ 但“查看权限是否生效”需要登录后才能看得更完整（模板里会显示 user/perms）
    """
    return render(request, "movies/perm_dashboard.html")

@login_required
def default_perms_api(request):
    """
    ✅ 返回 Movie 模型的默认权限（add/change/delete/view）
    同时讲清楚 app_label.codename 的命名规则。

    命名规则：
    - app_label：应用名（这里是 movies）
    - codename：动作_模型名小写，例如 add_movie
    - 组合成权限点：movies.add_movie
    """
    # 1) Movie 对应的 ContentType（权限归属到哪个模型靠它）
    ct = ContentType.objects.get_for_model(Movie)

    # 2) 找出该模型的默认权限（只取 add/change/delete/view）
    wanted = {"add_movie", "change_movie", "delete_movie", "view_movie"}

    perms = (
        Permission.objects
        .filter(content_type=ct, codename__in=wanted)
        .order_by("codename")
        .values("id", "name", "codename", "content_type__app_label")
    )

    # 3) 拼出 app_label.codename 的完整权限点字符串，方便学生理解
    data = []
    for p in perms:
        app_label = p["content_type__app_label"]
        codename = p["codename"]
        data.append({
            "id": p["id"],
            "name": p["name"],
            "app_label": app_label,
            "codename": codename,
            "perm_key": f"{app_label}.{codename}",  # ✅ movies.add_movie
        })

    return JsonResponse({"items": data})