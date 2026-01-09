from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("me/", views.me, name="me"),  # ✅ 角色/权限可视化页面
]