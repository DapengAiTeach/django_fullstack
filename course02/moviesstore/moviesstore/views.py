"""
首页视图文件

该文件定义了首页的视图函数。
"""

from django.shortcuts import render


def index_view(request):
    """
    首页视图
    
    显示网站首页，包括功能介绍和用户操作入口。
    
    Args:
        request: HTTP请求对象
        
    Returns:
        HttpResponse: 渲染首页
    """
    return render(request, 'index.html')
