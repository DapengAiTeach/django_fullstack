from django.contrib import admin
from django.urls import path, include
from movies import views as movie_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # 认证路由（本教程用 Django 自带登录视图）
    path("login/", movie_views.user_login, name="login"),
    path("logout/", movie_views.user_logout, name="logout"),

    # 业务路由
    path("", include("movies.urls")),
]