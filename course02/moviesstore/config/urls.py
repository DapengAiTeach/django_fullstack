from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # 电影应用路由，访问/movies/路径时，包含movies应用的URL路由
    path("movies/", include("movies.urls")),
]
