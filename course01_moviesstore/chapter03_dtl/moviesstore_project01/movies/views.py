from django.shortcuts import render

def home(request):
    # 模拟电影数据
    movies = [
        {'title': 'Inception', 'director': 'Christopher Nolan', 'year': 2010},
        {'title': 'Interstellar', 'director': 'Christopher Nolan', 'year': 2014},
        {'title': 'The Dark Knight', 'director': 'Christopher Nolan', 'year': 2008},
    ]
    # 渲染模板并传递数据
    return render(request, 'movies/home.html', {'movies': movies})