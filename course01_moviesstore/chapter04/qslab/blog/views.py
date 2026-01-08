from django.shortcuts import render, redirect
from django.db import connection
from django.db.models import Q
from .models import Article, Tag


def home(request):
    """
    首页：给学生一个入口 + 引导按钮
    """
    return render(request, "blog/home.html")


def seed(request):
    """
    一键造数据：方便课堂演示
    这里会创建一些标签与文章，并随机挂标签。
    """
    tag_names = ["Django", "ORM", "QuerySet", "性能", "前端", "MySQL"]
    tags = []
    for name in tag_names:
        t, _ = Tag.objects.get_or_create(name=name)
        tags.append(t)

    if Article.objects.count() < 20:
        for i in range(1, 21):
            a = Article.objects.create(
                title=f"第 {i} 篇：QuerySet 深度理解",
                views=i * 10,
                is_published=(i % 3 != 0),
            )
            # 给文章挂 1~3 个标签（演示 distinct/values_list 很好用）
            a.tags.add(tags[i % len(tags)])
            a.tags.add(tags[(i + 1) % len(tags)])
            if i % 2 == 0:
                a.tags.add(tags[(i + 2) % len(tags)])

    return redirect("blog:lab")


def _last_sql(limit=12):
    """
    取最近执行的 SQL（用于教学展示“什么时候真的访问 DB”）
    注意：只有 DEBUG=True 且 Django 记录 queries 时才能看到。
    """
    try:
        return connection.queries[-limit:]
    except Exception:
        return []


def query_lab(request):
    """
    QuerySet 实验室：用页面开关控制不同操作
    重点演示：
    - 惰性执行（创建 QuerySet 不会立刻查 DB）
    - 链式调用（filter().exclude().order_by()… 只是拼装 SQL）
    - QuerySet != List（QuerySet 是“查询表达式”，List 是“数据结果”）
    - 什么时候访问 DB（迭代、list()、len()、count()、exists()、first()、bool()等）

    典型能力：
    - values / values_list
    - distinct
    - exists
    - count
    """

    # --- 1) 构造 QuerySet（此时不访问 DB：惰性执行） ---
    qs = Article.objects.all()

    # 页面输入：关键字、是否只看发布、最小浏览量
    kw = request.GET.get("kw", "").strip()
    only_pub = request.GET.get("pub", "") == "1"
    min_views = request.GET.get("min_views", "").strip()

    # 链式调用：每一步都只是“追加条件”，不会立即执行 SQL
    if kw:
        qs = qs.filter(Q(title__icontains=kw))
    if only_pub:
        qs = qs.filter(is_published=True)
    if min_views.isdigit():
        qs = qs.filter(views__gte=int(min_views))

    # 可选：排除浏览量为 0（演示 exclude）
    if request.GET.get("ex0", "") == "1":
        qs = qs.exclude(views=0)

    # --- 2) 典型操作开关（这些会触发 DB） ---
    action = request.GET.get("action", "preview")
    payload = None

    # 为了课堂直观：每次处理前清一下 queries（更好观察）
    connection.queries_log.clear() if hasattr(connection, "queries_log") else None

    if action == "preview":
        """
        preview：展示前 10 条（触发 DB）
        触发点：qs[:10] 在模板迭代时会访问 DB
        """
        payload = qs[:10]

    elif action == "values":
        """
        values()：只取部分字段，返回 dict 序列（触发 DB 在迭代时）
        SQL: SELECT title, views ... FROM ...
        """
        payload = qs.values("id", "title", "views", "is_published")[:10]

    elif action == "values_list":
        """
        values_list()：只取部分字段，返回 tuple 序列
        flat=True 只在取单列时可用：会返回一维列表样式
        """
        payload = qs.values_list("title", "views")[:10]

    elif action == "distinct_tags":
        """
        distinct()：常见用法是“去重”
        这里演示：取所有文章的标签名去重
        """
        payload = (
            Tag.objects.filter(articles__in=qs)
            .values_list("name", flat=True)
            .distinct()
        )

    elif action == "exists":
        """
        exists()：最快判断“是否有数据”
        触发 DB：SELECT (1) ... LIMIT 1
        """
        payload = qs.exists()

    elif action == "count":
        """
        count()：数据库层 COUNT(*)
        触发 DB：SELECT COUNT(*) ...
        """
        payload = qs.count()

    # 最近 SQL（用于页面展示）
    sql_logs = _last_sql()

    return render(
        request,
        "blog/lab.html",
        {
            "kw": kw,
            "only_pub": only_pub,
            "min_views": min_views,
            "action": action,
            "payload": payload,
            "sql_logs": sql_logs,
            "qs_repr": repr(qs),  # 展示 QuerySet 表达式样子
        },
    )
