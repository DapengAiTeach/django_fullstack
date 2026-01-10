from decimal import Decimal
from django.contrib import admin
from django.core.exceptions import PermissionDenied

from apps.movies.models import Movie, Order, OrderItem
from apps.movies.forms import OrderItemInlineForm, OrderItemInlineFormSet


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "is_published"]
    list_editable = ["price", "is_published"]
    list_display_links = ["title"]
    search_fields = ["^title", "=id"]
    list_filter = ["is_published"]
    list_per_page = 20
    ordering = ["id"]


class OrderItemTabularInline(admin.TabularInline):
    """
    ✅ TabularInline：表格风格，最适合“订单明细/库存/配置项”这种高密度录入场景
    """
    model = OrderItem
    form = OrderItemInlineForm
    formset = OrderItemInlineFormSet

    # 行数控制
    extra = 1      # 默认给 1 行空白明细
    min_num = 1    # 至少 1 行（配合 formset.clean 再做后端强制）
    max_num = 5    # 最多 5 行（演示 UI 限制，后端还会校验总数量）

    can_delete = True          # 是否允许删除行
    show_change_link = True    # 子对象跳转链接

    # 让明细的计算字段只读（防篡改）
    readonly_fields = ["line_total"]

    fields = ["movie", "quantity", "unit_price", "line_total"]

    autocomplete_fields = ["movie"]  # 电影很多时用自动补全（推荐）

    def has_delete_permission(self, request, obj=None):
        """
        ✅ Inline 权限控制：只有超级用户可删除明细
        """
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        """
        ✅ Inline 性能优化：select_related + only 字段裁剪
        - movie 用到 title/price
        """
        qs = super().get_queryset(request)
        return qs.select_related("movie").only(
            "id", "order_id", "movie_id", "quantity", "unit_price", "line_total",
            "movie__id", "movie__title", "movie__price"
        )


class OrderItemStackedInline(admin.StackedInline):
    """
    ✅ StackedInline：卡片/分块风格，适合字段多、需要详细提示的明细
    本案例主要用 TabularInline，这里用作对比展示（你可以在 OrderAdmin 里切换）
    """
    model = OrderItem
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    订单主表 + Inline 明细：一次性录入与保存链路演示
    """
    list_display = ["id", "order_no", "customer_name", "status", "total_amount", "created_at"]
    list_display_links = ["order_no"]
    list_editable = ["status"]
    search_fields = ["^order_no", "customer_name"]
    list_filter = ["status", ("created_at", admin.DateFieldListFilter)]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_per_page = 20
    empty_value_display = "—"

    # ✅ 主表表单布局
    fieldsets = (
        ("订单信息", {
            "description": "创建订单后，在下方 Inline 一次性录入多条明细。",
            "fields": ("order_no", "customer_name", "status"),
        }),
        ("系统汇总", {
            "classes": ("collapse",),
            "fields": ("total_amount", "created_at"),
        }),
    )

    readonly_fields = ["total_amount", "created_at"]

    # ✅ 这里决定使用哪种 Inline
    inlines = [OrderItemTabularInline]  # 如果你要对比：改成 [OrderItemStackedInline]

    def get_readonly_fields(self, request, obj=None):
        """
        演示：订单编辑时，订单号不可修改（真实项目常见）
        """
        if obj is not None:
            return self.readonly_fields + ["order_no"]
        return self.readonly_fields

    def get_queryset(self, request):
        """
        ✅ 主表性能优化：prefetch items，并 select_related movie（列表页不显示 items，但你可扩展统计）
        """
        qs = super().get_queryset(request)
        return qs.only("id", "order_no", "customer_name", "status", "total_amount", "created_at")

    def save_formset(self, request, form, formset, change):
        """
        ✅ Inline 保存链路（很关键）：
        - 先拿到 formset 的实例
        - 对每一行明细：后端强制计算 line_total（防篡改）
        """
        instances = formset.save(commit=False)

        # 删除被勾选删除的对象
        for obj in formset.deleted_objects:
            obj.delete()

        for item in instances:
            # 防越权/防篡改：unit_price/quantity 来自表单，但 line_total 必须后端算
            qty = item.quantity or 0
            price = item.unit_price or Decimal("0.00")
            item.line_total = Decimal(qty) * price
            item.save()

        formset.save_m2m()

    def save_related(self, request, form, formsets, change):
        """
        ✅ 在 related 保存完之后，统一汇总订单总额 total_amount
        """
        super().save_related(request, form, formsets, change)

        order: Order = form.instance
        total = Decimal("0.00")
        # 这里 items 已经保存完成
        for it in order.items.all().only("line_total"):
            total += it.line_total or Decimal("0.00")

        order.total_amount = total
        order.save(update_fields=["total_amount"])