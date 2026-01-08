# movies/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Movie, CATEGORY_CHOICES

def home(request):
    # 首页直接跳搜索页也行，这里简单给个入口
    return render(request, "movies/home.html")


def search(request):
    """
    搜索页（重点）：
    ORM 不是 if else 去取数据，而是把“条件表达式”组合出来，然后一次性查询。
    """

    # 1) 先拿到 GET 参数（来自页面表单）
    kw = (request.GET.get("kw") or "").strip()  # 关键词
    min_rating = request.GET.get("min_rating")  # 最低评分
    max_rating = request.GET.get("max_rating")  # 最高评分
    categories = request.GET.getlist("cat")  # 多选分类（list）
    is_hot = request.GET.get("is_hot")  # "1" 或 None
    logic = request.GET.get("logic", "and")  # and / or（控制关键词的组合方式）

    # 2) 构造“基础 QuerySet”（惰性执行：还没查库）
    qs = Movie.objects.all()

    # 3) ⭐ 关键词：演示 __icontains + Q() + OR/AND 组合
    #    需求：kw 同时可以在 title/summary 中匹配
    if kw:
        # Q 条件：标题包含 OR 简介包含（最常用）
        kw_q = Q(title__icontains=kw) | Q(summary__icontains=kw)

        # 你也可以演示更复杂：如果逻辑选 or，允许“关键词 OR 热门”这种玩法
        # 这里把逻辑开关做成可控，学生会更有感觉
        if logic == "or":
            # 说明：此处不是 if/else 去查库，而是组合表达式
            # kw 匹配 OR is_hot=True（如果用户勾了热门开关）
            if is_hot == "1":
                qs = qs.filter(kw_q | Q(is_hot=True))
            else:
                qs = qs.filter(kw_q)
        else:
            # 默认 AND：先用关键词过滤
            qs = qs.filter(kw_q)

    # 4) 评分范围：__gte / __lte（数值/日期都一样的写法）
    #    注意：GET 是字符串，Django 会帮你做一定转换，但最好仍然做“存在性判断”
    if min_rating:
        qs = qs.filter(rating__gte=min_rating)
    if max_rating:
        qs = qs.filter(rating__lte=max_rating)

    # 5) 分类多选：__in
    if categories:
        qs = qs.filter(category__in=categories)

    # 6) 热门开关（如果没在关键词 logic=or 情况里处理，也可以在这里统一处理）
    if is_hot == "1" and logic != "or":
        qs = qs.filter(is_hot=True)

    # 7) 这里才会真正访问数据库：当模板遍历 qs、len(qs)、list(qs)、打印 qs 等
    movies = qs[:50]  # 做个上限，防止一次刷太多

    # 8) 把“当前筛选条件”回填给模板，便于表单保持状态
    context = {
        "movies": movies,
        "categories": CATEGORY_CHOICES,  # 👈 核心
        "kw": kw,
        "min_rating": min_rating or "",
        "max_rating": max_rating or "",
        "is_hot": is_hot or "",
        "logic": logic,
    }
    return render(request, "movies/search.html", context)
