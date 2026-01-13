from django.contrib import admin
from django.urls import path

# 首页视图函数
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    # 首页路由，访问根路径时，调用home视图函数
    path("", home, name="home"),
]
