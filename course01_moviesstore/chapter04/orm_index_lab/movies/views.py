# movies/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Movie
from .forms import MovieFilterForm

def home(request):
    return render(request, "movies/home.html")


def movie_index(request):
    """
    列表页：最容易产生慢查询的页面
    👉 因此这里的字段（category/is_active/created_at/title）都值得加索引
    """
    form = MovieFilterForm(request.GET or None)
    cleaned = {}
    if form.is_valid():
        cleaned = form.cleaned_data

    kw = (cleaned.get("kw") or "").strip()
    category = (cleaned.get("category") or "").strip()
    is_active = cleaned.get("is_active") or ""
    sort = cleaned.get("sort") or "-created_at"

    qs = Movie.objects.select_related("director")  # 外键：减少查询次数（顺便更快）

    # ✅ title 有 db_index（虽然 icontains 不一定走索引，但 kw 精确/前缀查询时很关键）
    if kw:
        qs = qs.filter(title__icontains=kw)

    # ✅ category 有 db_index + 复合索引(category, is_active)
    if category:
        qs = qs.filter(category=category)

    # ✅ is_active 有 db_index
    if is_active in ("0", "1"):
        qs = qs.filter(is_active=(is_active == "1"))

    # ✅ ordering 默认 -created_at，这里允许切换
    qs = qs.order_by(sort)

    movies = qs[:50]

    context = {
        "form": form,
        "movies": movies,
        "tips": [
            "category / is_active / created_at 常用于筛选排序，索引收益最大",
            "unique / unique_together 会变成唯一索引，能从根上防脏数据",
            "indexes 适合“高频组合条件”的后台列表页",
        ],
    }
    return render(request, "movies/movie_index.html", context)