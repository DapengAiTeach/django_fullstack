from django.shortcuts import render

# 导入响应对象
from django.http import HttpResponse

# 定义视图函数
def movie_list(request):
    """
    电影列表视图函数
    :param request: 请求对象
    :return: 响应对象
    """
    # 返回响应对象
    return HttpResponse("电影列表")