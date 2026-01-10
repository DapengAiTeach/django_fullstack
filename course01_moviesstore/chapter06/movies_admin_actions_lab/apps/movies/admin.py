from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render

from apps.movies.models import Movie, ActionLog
from apps.movies.forms import ChangeStatusForm


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "status", "created_by", "updated_at"]
    list_filter = ["status"]
    search_fields = ["^title"]
    list_per_page = 20

    actions = [
        "make_online",
        "make_offline",
    ]

    @admin.action(description="批量上架（无确认）")
    def make_online(self, request, queryset):
        """
        适用边界：简单状态流转
        """
        if not request.user.is_superuser:
            self.message_user(request, "只有超级用户可以执行该操作", level=messages.ERROR)
            return

        updated = queryset.update(status=3)

        ActionLog.objects.create(
            action="批量上架",
            operator=request.user,
            target_ids=",".join(str(i) for i in queryset.values_list("id", flat=True)),
        )

        self.message_user(request, f"成功上架 {updated} 条电影", level=messages.SUCCESS)

    @admin.action(description="批量下架（需要确认）")
    def make_offline(self, request, queryset):
        """
        规范 Action 写法：
        - 有确认页
        - 有表单
        - 有事务
        - 有日志
        """
        if not request.user.is_superuser:
            raise PermissionError("你没有权限执行该 Action")

        # 第一次进入：展示确认页
        if "apply" not in request.POST:
            form = ChangeStatusForm()
            return render(
                request,
                "admin/movies/movie/action_confirm.html",
                {
                    "movies": queryset,
                    "form": form,
                    "title": "确认批量下架",
                },
            )

        # 第二次提交：真正执行
        form = ChangeStatusForm(request.POST)
        if not form.is_valid():
            self.message_user(request, "表单校验失败", level=messages.ERROR)
            return

        if not form.cleaned_data["confirm"]:
            self.message_user(request, "必须勾选确认框", level=messages.WARNING)
            return

        remark = form.cleaned_data.get("remark", "")

        # === 事务处理 ===
        with transaction.atomic():
            for movie in queryset.select_for_update():
                movie.status = 4
                movie.save(update_fields=["status"])

            ActionLog.objects.create(
                action="批量下架",
                operator=request.user,
                target_ids=",".join(str(i) for i in queryset.values_list("id", flat=True)),
                remark=remark,
            )

        self.message_user(request, f"成功下架 {queryset.count()} 条电影", level=messages.SUCCESS)
