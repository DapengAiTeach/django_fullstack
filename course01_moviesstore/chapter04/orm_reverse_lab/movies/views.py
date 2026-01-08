# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg

from .models import Director, Movie, Review
from .forms import ReviewCreateForm


def home(request):
    return render(request, "movies/home.html")


def director_list(request):
    """
    导演列表：
    - annotate 演示：每个导演有多少部电影（反向统计）
    - 关键：Director 没有 movie_count 字段，但能点出来，因为 annotate “临时加字段”
    """
    qs = (
        Director.objects
        .annotate(movie_count=Count("movies"))  # ✅ 反向：Director -> movies(related_name) -> Count
        .order_by("-movie_count", "name")
    )
    return render(request, "movies/director_list.html", {"directors": qs})


def director_detail(request, pk):
    """
    导演详情：
    - 正向：Movie -> director
    - 反向：Director -> movies（related_name）
    """
    director = get_object_or_404(Director, pk=pk)

    # ✅ 反向查询：因为 Movie.director 写了 related_name="movies"
    # 所以导演对象可以：director.movies.all()
    movies = director.movies.order_by("-created_at")

    # 反向聚合：导演旗下电影的平均评分（来自 Review，通过跨表）
    # Director -> movies -> review_set（默认反向名） -> Avg(score)
    stat = director.movies.aggregate(avg_score=Avg("review__score"))  # ✅ 跨表字段写法

    return render(
        request,
        "movies/director_detail.html",
        {"director": director, "movies": movies, "avg_score": stat["avg_score"]},
    )


def movie_detail(request, pk):
    """
    电影详情页：
    - 展示评论（反向：movie.review_set）
    - 提交评论（创建 Review 记录）
    """
    movie = get_object_or_404(Movie.objects.select_related("director"), pk=pk)

    # ✅ 默认反向访问方式：Review.movie 没写 related_name，所以默认是 review_set
    reviews = movie.review_set.order_by("-created_at")

    form = ReviewCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Review.objects.create(
            movie=movie,
            nickname=form.cleaned_data["nickname"],
            score=form.cleaned_data["score"],
            content=form.cleaned_data["content"],
        )
        return redirect("movies:movie_detail", pk=movie.pk)

    return render(
        request,
        "movies/movie_detail.html",
        {"movie": movie, "reviews": reviews, "form": form},
    )