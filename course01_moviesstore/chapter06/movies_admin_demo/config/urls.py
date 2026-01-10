from django.contrib import admin
from django.urls import path, include
from apps.accounts.admin_branding import apply_admin_branding

from apps.accounts.admin_sites import ops_site  # ✅ 自定义运营后台 AdminSite

urlpatterns = [
    path("admin/", admin.site.urls),      # 技术后台（默认 AdminSite）
    path("ops/", ops_site.urls),          # 运营后台（自定义 AdminSite）
    path("", include("apps.movies.urls")),  # ✅ 前台入口
]

apply_admin_branding(
    admin.site,
    header="技术后台 · Movies Admin Demo",
    title="技术后台",
    index_title="数据与权限管理",
)