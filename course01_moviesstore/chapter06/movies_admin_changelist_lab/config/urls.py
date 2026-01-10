from django.contrib import admin
from django.urls import path, include

from apps.accounts.admin_branding import apply_admin_branding

apply_admin_branding(
    admin.site,
    header="技术后台 · Changelist Lab",
    title="Changelist Lab",
    index_title="列表页深度定制演示",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]