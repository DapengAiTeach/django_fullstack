from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from apps.movies.models import Genre, Director, Movie
from apps.movies.forms import MovieAdminForm
from apps.movies.admin_filters import ScoreLevelFilter, PriceRangeFilter
from apps.movies.admin_tools import FastCountPaginator


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["^name"]
    list_display = ["id", "name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ["^name"]
    list_display = ["id", "name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    ✅ 列表页深度定制（Changelist）
    """

    form = MovieAdminForm

    # --- Changelist 基础组件：展示字段（含图片/徽章/链接/颜色） ---
    list_display = [
        "id",
        "poster_preview",
        "title_link",
        "genre",
        "director",
        "price",
        "score_colored",
        "status_badge",
        "created_by",
        "created_at",
    ]
    list_display_links = None  # ✅ 我们用 title_link 自己做链接，因此这里设为 None

    # --- filters/search/pagination ---
    search_fields = ["^title", "genre__name", "director__name"]
    list_filter = [
        "status",
        "genre",
        "director",
        ScoreLevelFilter,
        PriceRangeFilter,
        ("created_at", admin.DateFieldListFilter),
    ]
    date_hierarchy = "created_at"
    list_per_page = 20
    ordering = ["-created_at"]
    empty_value_display = "—"

    # --- N+1 优化：外键列表页必备 ---
    list_select_related = ["genre", "director", "created_by"]

    # --- 关闭精确 count：减少“结果总数”带来的压力（尤其大表） ---
    show_full_result_count = False

    # --- 自定义分页器（演示） ---
    paginator = FastCountPaginator

    # --- 自定义列表页模板（change_list_template） ---
    change_list_template = "admin/movies/movie/change_list.html"

    # --- 注入 CSS，让列表页更像“运营系统” ---
    class Media:
        css = {"all": ("admin_ext/css/changelist_lab.css",)}

    # ---------------------------
    # 1) get_queryset：权限裁剪 + 性能优化 + 字段裁剪
    # ---------------------------
    def get_queryset(self, request):
        """
        ✅ 权限裁剪策略（演示）：
        - superuser：看全部
        - staff：只看自己创建的（created_by=request.user）
        同时做性能优化：
        - select_related（外键）
        - only 字段裁剪（大表非常关键）
        """
        qs = super().get_queryset(request)

        qs = qs.select_related("genre", "director", "created_by").only(
            "id", "title", "price", "score", "status", "poster_url",
            "created_at", "created_by__username",
            "genre__name", "director__name",
        )

        if request.user.is_superuser:
            return qs

        # staff 才能进 admin，演示：只看自己创建的
        return qs.filter(created_by=request.user)

    # ---------------------------
    # 2) get_search_results：自定义业务搜索（组合搜索/结构化搜索）
    # ---------------------------
    def get_search_results(self, request, queryset, search_term):
        """
        ✅ 在默认搜索基础上增加“结构化语法”，运营同学更爱用：
        - g:科幻      => 按类型搜索
        - d:诺兰      => 按导演搜索
        - status:3    => 按运营状态（3=已上架）
        - score>=8.5  => 高分筛选
        - 纯数字      => 视为 ID 精确搜索
        其余文本：按 title contains（业务更符合习惯）
        """
        qs, use_distinct = super().get_search_results(request, queryset, search_term)

        term = (search_term or "").strip()
        if not term:
            return qs, use_distinct

        tokens = term.split()
        extra_q = Q()

        for t in tokens:
            if t.isdigit():
                extra_q &= Q(id=int(t))
                continue

            if t.startswith("g:"):
                v = t[2:].strip()
                if v:
                    extra_q &= Q(genre__name__icontains=v)
                continue

            if t.startswith("d:"):
                v = t[2:].strip()
                if v:
                    extra_q &= Q(director__name__icontains=v)
                continue

            if t.startswith("status:"):
                v = t[7:].strip()
                if v.isdigit():
                    extra_q &= Q(status=int(v))
                continue

            if t.startswith("score>="):
                v = t[7:].strip()
                try:
                    extra_q &= Q(score__gte=float(v))
                except ValueError:
                    pass
                continue

            # 普通关键词：更偏业务习惯（包含匹配）
            extra_q &= Q(title__icontains=t)

        return qs.filter(extra_q), use_distinct

    # ---------------------------
    # 3) 列表页展示增强：图片预览、链接、徽章、颜色
    # ---------------------------
    @admin.display(description="海报")
    def poster_preview(self, obj: Movie):
        """
        ✅ 图片预览：用 poster_url（不依赖 MEDIA）
        """
        if not obj.poster_url:
            return "—"
        return format_html('<img class="clb-thumb" src="{}" alt="poster" />', obj.poster_url)

    @admin.display(description="片名")
    def title_link(self, obj: Movie):
        """
        ✅ 自定义链接：可跳转到编辑页
        """
        return format_html('<a href="{}"><b>{}</b></a>', f"./{obj.id}/change/", obj.title)

    @admin.display(description="评分", ordering="score")
    def score_colored(self, obj: Movie):
        """
        ✅ 颜色提示：评分越高越“绿”，越低越“橙/灰”
        """
        s = float(obj.score or 0)
        if s >= 8.5:
            cls = "clb-badge clb-green"
        elif s >= 7.5:
            cls = "clb-badge clb-blue"
        elif s >= 6.5:
            cls = "clb-badge clb-orange"
        else:
            cls = "clb-badge clb-gray"
        return format_html('<span class="{}">{}</span>', cls, f"{s:.1f}")

    @admin.display(description="状态", ordering="status")
    def status_badge(self, obj: Movie):
        """
        ✅ 徽章：运营状态一眼可读
        """
        mapping = {
            1: ("草稿", "clb-gray"),
            2: ("待上架", "clb-orange"),
            3: ("已上架", "clb-green"),
            4: ("已下架", "clb-red"),
        }
        text, cls = mapping.get(obj.status, ("未知", "clb-gray"))
        return format_html('<span class="clb-badge {}">{}</span>', cls, text)