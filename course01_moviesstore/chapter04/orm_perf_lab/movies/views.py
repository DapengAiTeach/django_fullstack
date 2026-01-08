# movies/views.py
import time
from django.conf import settings
from django.db import connection
from django.db.models import Count
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from .models import Movie, Review
from .forms import FeedModeForm


def home(request):
    return render(request, "movies/home.html")


def _sql_stats():
    """
    开发环境统计 SQL 次数与总耗时（仅 DEBUG=True 有意义）
    connection.queries 由 Django 记录，每条包含 sql 与 time。
    """
    if not settings.DEBUG:
        return {"count": "-", "time_ms": "-"}
    total_ms = 0.0
    for q in connection.queries:
        # q["time"] 是字符串秒数
        total_ms += float(q.get("time", 0)) * 1000
    return {"count": len(connection.queries), "time_ms": round(total_ms, 2)}


def movie_feed(request):
    """
    电影信息流：展示
    - 标题
    - 导演（FK）
    - 标签（M2M）
    - 最新3条评论（FK反向）
    这是 N+1 最爱发生的组合。
    """
    form = FeedModeForm(request.GET or None)
    mode = "fast"
    if form.is_valid():
        mode = form.cleaned_data.get("mode") or "fast"

    # 统计开始前清空 queries（便于页面展示“本次请求”的 SQL 数）
    if settings.DEBUG:
        connection.queries_log.clear() if hasattr(connection, "queries_log") else None
        connection.queries.clear()

    t0 = time.perf_counter()

    movies = Movie.objects.all().order_by("-created_at")[:20]

    if mode == "slow":
        # ❌ 慢：不做任何优化
        # 模板里访问 m.director、m.tags、m.reviews 都会触发额外查询（N+1）
        pass

    elif mode == "fast":
        # ✅ 快：一对多/一对一用 select_related；多对多/反向集合用 prefetch_related
        # 1) director：FK => select_related（JOIN 一次搞定）
        # 2) tags：M2M => prefetch_related（额外一次查询+内存拼装）
        # 3) reviews：反向 FK => 用 Prefetch 限制只取最新3条（避免把全部评论都拉出来）
        latest_reviews_qs = Review.objects.order_by("-created_at")
        movies = (
            Movie.objects
            .select_related("director")
            .prefetch_related("tags")
            .prefetch_related(Prefetch("reviews", queryset=latest_reviews_qs, to_attr="latest_reviews"))
            .order_by("-created_at")[:20]
        )

    elif mode == "split":
        # ✅ 拆分：列表页“只显示统计信息”，不要显示评论详情
        # 列表页经常只要：评论数/平均分，而不是把每条评论都渲染出来
        movies = (
            Movie.objects
            .select_related("director")
            .prefetch_related("tags")
            .annotate(review_count=Count("reviews"))
            .order_by("-created_at")[:20]
        )
        # 需要详情时再点进 movie_detail（合理拆分查询）

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
    stats = _sql_stats()

    return render(
        request,
        "movies/movie_feed.html",
        {
            "form": form,
            "mode": mode,
            "movies": movies,
            "elapsed_ms": elapsed_ms,
            "sql_count": stats["count"],
            "sql_time_ms": stats["time_ms"],
        },
    )


def movie_detail(request, pk):
    """
    详情页：这里可以“更重”一点，因为是单页。
    """
    movie = get_object_or_404(
        Movie.objects.select_related("director").prefetch_related("tags", "reviews"),
        pk=pk
    )
    return render(request, "movies/movie_detail.html", {"movie": movie})