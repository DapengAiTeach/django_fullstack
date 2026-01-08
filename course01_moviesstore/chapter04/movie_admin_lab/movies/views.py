# movies/views.py
from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Max, Min
from django.core.paginator import Paginator
from django.utils.http import urlencode

from .models import Movie
from .forms import MovieAdminFilterForm


def home(request):
    return render(request, "movies/home.html")


def movie_admin_list(request):
    """
    这是后台系统/列表页最核心的能力：
    - QuerySet 先过滤（GET 表单）
    - 再排序 order_by()
    - 再聚合 aggregate() / annotate()
    - 最后分页 Paginator（并保留查询参数实现联动）
    """

    form = MovieAdminFilterForm(request.GET)

    cleaned = {}
    if form.is_valid():
        cleaned = form.cleaned_data

    kw = (cleaned.get("kw") or "").strip()
    category = cleaned.get("category") or ""
    sort = cleaned.get("sort") or "-created_at"
    page_size = int(cleaned.get("page_size") or 10)

    qs = Movie.objects.all()

    if kw:
        qs = qs.filter(title__icontains=kw)
    if category:
        qs = qs.filter(category=category)

    qs = qs.order_by(sort)

    # 5) ✅ 聚合：aggregate()（对“当前筛选结果集”做统计）
    # 注意：aggregate 返回 dict；不会改变 qs
    stats = qs.aggregate(
        total=Count("id"),
        stock_sum=Sum("stock"),
        price_sum=Sum("price"),
        price_avg=Avg("price"),
        rating_avg=Avg("rating"),
        rating_max=Max("rating"),
        rating_min=Min("rating"),
    )

    # 6) ✅ 分组聚合：annotate()（为每个分类算数量）
    # 这是“列表页顶部统计卡片/图表”的常用数据来源
    by_category = (
        qs.values("category")
        .annotate(c=Count("id"), avg_rating=Avg("rating"))
        .order_by("-c")
    )

    # 7) ✅ 分页：Paginator（对 qs 分页）
    paginator = Paginator(qs, page_size)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)  # get_page 更友好：越界会自动修正

    # 8) 分页联动关键：保留除了 page 之外的所有查询参数
    # 用于模板里生成 ?kw=...&category=...&sort=...&page=2
    querydict = request.GET.copy()
    querydict.pop("page", None)
    base_qs = querydict.urlencode()  # 已经是 a=b&c=d 形式

    context = {
        "form": form,
        "page_obj": page_obj,
        "stats": stats,
        "by_category": by_category,
        "base_qs": base_qs,
    }
    return render(request, "movies/movie_admin_list.html", context)
