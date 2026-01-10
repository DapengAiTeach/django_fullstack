from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "电影后台 · UI Lab"
admin.site.site_title = "Admin UI Lab"
admin.site.index_title = "Admin 模板体系与 UI 定制"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.movies.urls")),
]