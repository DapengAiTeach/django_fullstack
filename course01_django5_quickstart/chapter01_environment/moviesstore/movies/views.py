from django.shortcuts import render

def index(request):
    """电影商城首页视图"""
    return render(request, 'movies/index.html')
