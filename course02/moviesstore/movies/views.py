from django.shortcuts import render

# 定义视图函数
def movie_list(request):
    """
    电影列表视图函数
    :param request: 请求对象
    :return: 响应对象
    """
    # 返回渲染页面
    return render(request, 'movies/movie_list.html')
