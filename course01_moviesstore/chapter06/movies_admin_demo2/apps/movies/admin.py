from django.contrib import admin
from django.utils.html import format_html

from apps.movies.models import Genre, Director, Tag, Movie
from apps.movies.forms import MovieAdminForm


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["^name"]  # ✅ '^' 前缀匹配更快


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["^name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """
    ✅ autocomplete_fields 前置条件：
    被自动补全引用的模型必须配置 search_fields，否则 Django 会报错。
    """
    list_display = ["id", "name", "country"]
    search_fields = ["^name", "country"]
    list_per_page = 20


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    目标：讲透 ModelAdmin 基础字段配置（你列的全部点）
    """
    form = MovieAdminForm

    # =========================
    # 1) list_display：列表展示字段与方法字段
    # =========================
    list_display = [
        "id",
        "title",
        "genre",
        "director",
        "price",
        "level",  # ✅ 真实字段：为了 list_editable
        "level_badge",  # ✅ 方法字段：为了更好看（可选）
        "is_published",
        "stock",
        "created_at",
    ]

    @admin.display(description="运营等级", ordering="level")
    def level_badge(self, obj: Movie):
        """
        ✅ 方法字段：用徽章提升可读性
        - description：列名
        - ordering：允许按 level 排序
        """
        mapping = {
            1: ("A级", "#3b82f6"),
            2: ("S级", "#10b981"),
            3: ("SS级", "#f59e0b"),
        }
        text, color = mapping.get(obj.level, ("未知", "#6b7280"))
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:999px;background:{};color:#fff;font-size:12px;">{}</span>',
            color,
            text,
        )

    # =========================
    # 2) list_display_links：控制点击进入详情的字段
    # =========================
    list_display_links = ["title"]  # ✅ 推荐只让标题可点，避免误触

    # =========================
    # 3) list_editable：列表页快速编辑（限制与坑）
    # =========================
    # ⚠️ 坑1：list_editable 的字段不能同时出现在 list_display_links
    # ⚠️ 坑2：list_editable 的字段也不能是 list_display 的第一列
    list_editable = ["price", "is_published", "stock", "level"]

    # =========================
    # 4) list_per_page / list_max_show_all：分页与性能
    # =========================
    list_per_page = 20
    list_max_show_all = 200  # ✅ 避免一次性显示全部导致卡死

    # =========================
    # 5) ordering：默认排序策略（含关联字段排序技巧）
    # =========================
    ordering = ["-created_at", "genre__name", "director__name"]  # ✅ 关联字段排序写法

    # =========================
    # 6) search_fields：搜索字段（^ = @）
    # =========================
    # '^'：前缀匹配（通常更快，适合名称/编号）
    # '='：精确匹配（适合唯一字段）
    # '@'：全文检索（依赖数据库支持与全文索引配置）
    search_fields = [
        "^title",            # ✅ 前缀匹配：输入“星际”更快命中
        "=id",               # ✅ 精确匹配：输入 12 直接命中 ID=12（演示用）
        "genre__name",       # 关联字段 contains
        "director__name",    # 关联字段 contains
        # "@title",          # ⚠️ MySQL 需全文索引，SQLite 没有真正全文检索，这里先注释
    ]

    # =========================
    # 7) list_filter：右侧筛选（字段筛选 / 自定义筛选器）
    # =========================
    list_filter = [
        "is_published",
        "genre",
        "level",
        ("created_at", admin.DateFieldListFilter),  # ✅ 日期筛选更友好
    ]

    # =========================
    # 8) date_hierarchy：日期层级导航
    # =========================
    date_hierarchy = "created_at"

    # =========================
    # 9) empty_value_display：空值展示统一风格
    # =========================
    empty_value_display = "—"

    # =========================
    # 10) fields / fieldsets：表单字段布局（分组、折叠、描述）
    # =========================
    fieldsets = (
        ("基础信息", {
            "description": "决定商品展示与检索的核心字段（标题、类型、导演、标签）。",
            "fields": ("title", "genre", "director", "tags"),
        }),
        ("运营配置", {
            "description": "运营同学高频调整字段：价格、等级、上下架、库存。",
            "fields": ("price", "level", "is_published", "stock"),
        }),
        ("系统信息", {
            "classes": ("collapse",),  # ✅ 折叠区域
            "fields": ("created_at",),
        }),
    )

    # =========================
    # 11) readonly_fields：只读字段与动态只读
    # =========================
    readonly_fields = ["created_at"]

    def get_readonly_fields(self, request, obj=None):
        """
        ✅ 动态只读：
        - 新增时允许改 title
        - 编辑时禁止改 title（避免商品标题被误改）
        """
        if obj is not None:
            return self.readonly_fields + ["title"]
        return self.readonly_fields

    # =========================
    # 12) exclude：排除字段
    # =========================
    # 演示：如果你不想让运营改库存，可以排除 stock
    # 这里不排除，保证功能完整
    # exclude = ["stock"]

    # =========================
    # 13) raw_id_fields：外键输入框替换下拉（大数据量必备）
    # =========================
    # 演示：当导演数据量非常大时启用（与 autocomplete 二选一更常见）
    # raw_id_fields = ["director"]

    # =========================
    # 14) autocomplete_fields：外键自动补全（推荐）
    # =========================
    autocomplete_fields = ["director", "genre"]

    # =========================
    # 15) filter_horizontal / filter_vertical：ManyToMany 选择器
    # =========================
    filter_horizontal = ["tags"]  # ✅ 标签双栏选择器更好用

    # =========================
    # 16) radio_fields：枚举/外键使用单选（UI 优化）
    # =========================
    radio_fields = {"level": admin.VERTICAL}

    # ✅ 性能优化：列表页显示外键时避免 N+1
    list_select_related = ["genre", "director"]