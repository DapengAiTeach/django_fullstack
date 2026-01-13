"""
用户视图文件

该文件定义了用户相关的视图函数，包括注册、登录、登出、个人信息等。
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import transaction

from .forms import UserRegisterForm, UserProfileForm, UserLoginForm
from .models import User


class RegisterView:
    """
    用户注册视图
    
    处理用户注册请求，包括GET和POST方法。
    """
    
    @staticmethod
    def get(request):
        """
        处理GET请求
        
        显示注册表单页面。
        
        Args:
            request: HTTP请求对象
            
        Returns:
            HttpResponse: 渲染注册页面
        """
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    @staticmethod
    def post(request):
        """
        处理POST请求
        
        处理用户注册表单提交，验证数据并创建用户。
        
        Args:
            request: HTTP请求对象
            
        Returns:
            HttpResponse: 注册成功重定向到登录页面，失败则显示错误信息
        """
        form = UserRegisterForm(request.POST, request.FILES)
        
        # 验证表单数据
        if form.is_valid():
            try:
                # 使用事务确保数据一致性
                with transaction.atomic():
                    # 创建用户
                    user = form.save()
                    
                    # 添加成功消息
                    messages.success(request, '注册成功！请登录。')
                    
                    # 重定向到登录页面
                    return redirect(reverse('users:login'))
            except Exception as e:
                # 添加错误消息
                messages.error(request, f'注册失败：{str(e)}')
        
        # 表单验证失败，显示错误信息
        return render(request, 'users/register.html', {'form': form})


class LoginView(BaseLoginView):
    """
    用户登录视图
    
    继承自Django的LoginView，自定义模板和重定向。
    """
    
    template_name = 'users/login.html'  # 指定登录页面模板
    redirect_authenticated_user = True  # 已登录用户重定向到首页
    authentication_form = UserLoginForm  # 使用自定义的登录表单
    
    def get_success_url(self):
        """
        获取登录成功后的重定向URL
        
        Returns:
            str: 重定向URL
        """
        # 获取next参数，如果有则重定向到next指定的页面
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        # 否则重定向到首页
        return reverse_lazy('index')


class LogoutView(BaseLogoutView):
    """
    用户登出视图
    
    继承自Django的LogoutView，自定义重定向。
    """
    
    next_page = reverse_lazy('index')  # 登出后重定向到首页


@login_required
def profile_view(request):
    """
    个人信息视图
    
    显示和编辑用户个人信息。
    
    Args:
        request: HTTP请求对象
        
    Returns:
        HttpResponse: 渲染个人信息页面
    """
    # 获取当前用户
    user = request.user
    
    if request.method == 'POST':
        # 处理个人信息修改
        # 直接更新用户字段
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.birthday = request.POST.get('birthday')
        user.gender = request.POST.get('gender')
        user.bio = request.POST.get('bio')
        user.save()
        
        messages.success(request, '个人信息更新成功！')
        return redirect(reverse('users:profile'))
    
    return render(request, 'users/profile.html', {'user': user})


def register_view(request):
    """
    用户注册视图函数
    
    根据请求方法调用对应的处理函数。
    
    Args:
        request: HTTP请求对象
        
    Returns:
        HttpResponse: 渲染注册页面或重定向
    """
    if request.method == 'POST':
        return RegisterView.post(request)
    else:
        return RegisterView.get(request)
