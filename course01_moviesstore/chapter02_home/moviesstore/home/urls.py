from django.urls import path
from . import views

# 名称空间
app_name = 'home'

urlpatterns = [
    # 首页路由
    path('', views.index, name='index'),
]