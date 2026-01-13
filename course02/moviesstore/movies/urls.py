from django.urls import path
from .views import movie_list

# 定义应用的URL路由
urlpatterns = [
    # 电影列表路由，访问/路径时，调用movie_list视图函数
    path("", movie_list, name="movie_list"),
]