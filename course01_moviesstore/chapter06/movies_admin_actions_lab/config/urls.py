from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "电影后台 · Actions Lab"
admin.site.site_title = "Actions Lab"
admin.site.index_title = "批量操作与审计"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]