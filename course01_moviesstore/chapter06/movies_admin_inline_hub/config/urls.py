from django.contrib import admin
from django.urls import path, include

from apps.accounts.admin_branding import apply_admin_branding

apply_admin_branding(
    admin.site,
    header="技术后台 · Inline Hub",
    title="Inline Hub",
    index_title="主表+明细一次性录入演示",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]