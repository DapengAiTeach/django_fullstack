from django.contrib import admin
from django.urls import path, include

from apps.accounts.admin_branding import apply_admin_branding

apply_admin_branding(
    admin.site,
    header="技术后台 · Admin Forms Lab",
    title="Admin Forms Lab",
    index_title="表单深度定制演示台",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]