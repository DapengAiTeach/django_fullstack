"""
用户应用URL路由配置文件

该文件定义了用户应用的所有URL路由规则。
"""

from django.urls import path
from . import views

# URL模式列表
# 使用namespace='users'来避免URL名称冲突
app_name = 'users'

urlpatterns = [
    # 注册页面
    # 访问 /users/register/ 会显示注册页面
    path('register/', views.register_view, name='register'),
    
    # 登录页面
    # 访问 /users/login/ 会显示登录页面
    path('login/', views.LoginView.as_view(), name='login'),
    
    # 登出页面
    # 访问 /users/logout/ 会执行登出操作
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # 个人信息页面
    # 访问 /users/profile/ 会显示个人信息页面
    path('profile/', views.profile_view, name='profile'),
]
