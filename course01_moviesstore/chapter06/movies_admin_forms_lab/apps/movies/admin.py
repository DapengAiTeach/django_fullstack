from decimal import Decimal
from django.contrib import admin
from django.core.exceptions import PermissionDenied

from apps.movies.models import Movie
from apps.movies.forms import MovieCreateForm, MovieChangeForm


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    本章目标：Admin 表单深度定制
    - form：绑定自定义 ModelForm
    - get_form()：按 request/user/obj 动态切换表单
    - clean_<field>() / clean()：在 forms.py 中完成
    - widget/attrs/help_text：在 forms.py 的 Meta 中完成
    - 新增/编辑差异：readonly_fields + get_form + fieldsets
    - Media：注入 JS/CSS 做联动（折扣改变时实时计算最终价）
    - 防御性校验：隐藏字段篡改、越权字段提交
    """

    # ✅ 列表页让运营同学能快速处理
    list_display = ["id", "title", "price", "discount", "final_price", "is_published", "risk_level", "created_at"]
    list_display_links = ["title"]
    list_editable = ["price", "discount", "is_published"]  # ✅ 行内编辑（risk_level 不给行内编辑）
    search_fields = ["^title", "=id"]
    list_filter = ["is_published", "risk_level", ("created_at", admin.DateFieldListFilter)]
    date_hierarchy = "created_at"
    list_per_page = 20
    list_max_show_all = 200
    ordering = ["-created_at"]
    empty_value_display = "—"

    # ✅ 表单布局：分组 + 折叠
    fieldsets = (
        ("基础信息", {
            "description": "运营维护的核心字段：标题、价格、折扣、上下架。",
            "fields": ("title", "price", "discount", "final_price", "is_published"),
        }),
        ("风控信息（仅管理员）", {
            "classes": ("collapse",),
            "fields": ("risk_level",),
        }),
        ("系统信息", {
            "classes": ("collapse",),
            "fields": ("created_by", "created_at"),
        }),
    )

    # ✅ 只读字段（final_price 必须只读，created_by/created_at 也只读）
    readonly_fields = ["final_price", "created_by", "created_at"]

    def get_readonly_fields(self, request, obj=None):
        """
        ✅ 新增/编辑差异处理：
        - 编辑时 title 只读，避免误改
        """
        if obj is not None:
            return self.readonly_fields + ["title"]
        return self.readonly_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        ✅ 动态切换表单（按请求/用户/对象）
        - 新增：MovieCreateForm
        - 编辑：MovieChangeForm
        - 非超级用户：强制把 risk_level 变成只读（并且后端防越权）
        """
        if obj is None:
            kwargs["form"] = MovieCreateForm
        else:
            kwargs["form"] = MovieChangeForm

        form_class = super().get_form(request, obj, change, **kwargs)

        # ✅ 进一步动态改字段：普通 staff 不允许改 risk_level
        if not request.user.is_superuser and "risk_level" in form_class.base_fields:
            # 这里做 UI 限制（readonly_fields 已经只读，但我们再加强：禁用）
            form_class.base_fields["risk_level"].disabled = True
            form_class.base_fields["risk_level"].help_text = "仅超级用户可修改（已锁定）。"

        return form_class

    def save_model(self, request, obj: Movie, form, change):
        """
        ✅ 防御性校验（后端强制）：
        1) created_by：无论前端提交什么，后端强制写入当前用户（防隐藏字段篡改）
        2) final_price：永远由后端计算（防篡改）
        3) risk_level：普通用户即使抓包提交也不允许改（防越权）
        """
        # 1) created_by 防篡改：新增时写入创建人
        if not change and obj.created_by_id is None:
            obj.created_by = request.user

        # 2) final_price 防篡改：永远后端计算
        price = obj.price or Decimal("0")
        discount = obj.discount or 0
        obj.final_price = price * (Decimal(100) - Decimal(discount)) / Decimal(100)

        # 3) risk_level 防越权：非超级用户禁止改
        if change and not request.user.is_superuser:
            # 从数据库取旧值，对比是否被改动（即使表单禁用，也要后端核验）
            old = Movie.objects.get(pk=obj.pk)
            if obj.risk_level != old.risk_level:
                raise PermissionDenied("你没有权限修改风控等级 risk_level（已拦截越权提交）。")

        super().save_model(request, obj, form, change)

    class Media:
        """
        ✅ Media：注入 JS/CSS，让表单有联动体验
        - discount 或 price 改变时，实时刷新 final_price 展示（只读字段也能动态显示）
        """
        css = {"all": ("admin_ext/css/admin_forms_lab.css",)}
        js = ("admin_ext/js/movie_form_linkage.js",)