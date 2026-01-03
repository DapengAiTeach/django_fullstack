from django.urls import path
from movies import views

urlpatterns = [
    path('', views.home, name='home'),  # 首页路由
]