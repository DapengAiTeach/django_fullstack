from django.contrib import admin
from django.urls import path, include

from apps.accounts.admin_branding import apply_admin_branding

# ✅ Admin 站点品牌化（让后台更像真实系统）
apply_admin_branding(
    admin.site,
    header="技术后台 · Movies Admin Demo",
    title="技术后台",
    index_title="数据与权限管理",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]